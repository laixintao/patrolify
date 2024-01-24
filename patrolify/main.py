import sys
import importlib
import waitress
import importlib.util
import logging
import os
import pathlib

import click
from redis import Redis
from rq import Queue, Worker

from rq_scheduler import Scheduler

from .globals import Role, g
from .reports import generate_report
from .admin import create_app
from patrolify import __version__


logger = logging.getLogger(__name__)
LOG_LEVEL = {
    0: logging.CRITICAL,
    1: logging.WARNING,
    2: logging.INFO,
    3: logging.DEBUG,
}


def setup_log(enabled, level, loglocation):
    if enabled:
        logging.basicConfig(
            filename=os.path.expanduser(loglocation),
            filemode="a",
            format="%(asctime)s %(levelname)5s (%(module)sL%(lineno)d) %(message)s",
            level=level,
        )
    else:
        logging.disable(logging.CRITICAL)
    logger.info("------ patrolify ------")


def load_checkers(path):
    sys.path.append(str(pathlib.Path(path).parent))
    for root, _, files in os.walk(path):
        for file in files:
            abs_path = os.path.join(root, file)
            if not file.endswith(".py"):
                logger.debug("%s is not ending with .py, ignore...", abs_path)
                continue
            logger.info("import python file: %s", abs_path)

            # remove the ./ prefix
            abs_path = abs_path.lstrip("./")

            module_name = abs_path[:-3].replace("/", ".")
            logger.info("loading module: %s", module_name)
            importlib.import_module(module_name)
    logger.info("Loading checkers done: %s", g.target_checkers)


def print_version(ctx, _, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__)
    ctx.exit()


@click.group()
@click.option(
    "-v",
    "--verbose",
    count=True,
    default=2,
    help="Add log verbose level, using -v, -vv, -vvv for printing more logs.",
)
@click.option(
    "-l",
    "--log-to",
    type=click.Path(),
    default=None,
    help="Printing logs to a file, for debugging, default is no logs.",
)
@click.option("-r", "--redis-url", help="Redis url as the job queue")
@click.option(
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
)
def main(verbose, log_to, redis_url):
    log_level = LOG_LEVEL[verbose]
    setup_log(log_to is not None, log_level, log_to)
    g.redis = Redis.from_url(redis_url)
    g.checker_queue = Queue("checker", connection=g.redis)
    g.reporter_queue = Queue("reporter", connection=g.redis)


@main.command()
@click.option(
    "-p",
    "--python-checker",
    type=click.Path(),
    default=None,
    help="Python checker script location",
)
@click.option(
    "-r",
    "--result-path",
    type=click.Path(),
    default=None,
    help="Where to save the results",
)
@click.option(
    "--queue",
    "-q",
    multiple=True,
    help=(
        "work for which queue? queue type: 1) checker 2) patrolify, for generating"
        " reports. If you use the file system as the report store, you should only run"
        " one worker for the patrolify queue."
    ),
)
def worker(python_checker, result_path, queue):
    queue_map = {
        "checker": g.checker_queue,
        "reporter": g.reporter_queue,
    }

    _queue = []
    for item in queue:
        if item not in queue_map:
            raise click.UsageError(
                f"Queue {item} not in {','.join(queue_map.keys())}", ctx=None
            )
        _queue.append(queue_map[item])

    g.role = Role.WORKER
    g.result_path = pathlib.Path(result_path)
    load_checkers(python_checker)
    start_worker(_queue)


@main.command()
@click.option(
    "-p",
    "--python-checker",
    type=click.Path(),
    default=None,
    help="Python checker script location",
)
def planner(python_checker):
    g.role = Role.PLANNER
    g.scheduler = Scheduler(
        queue=g.checker_queue, connection=g.checker_queue.connection
    )

    # cancel the existing jobs
    list_of_job_instances = g.scheduler.get_jobs()
    for j in list_of_job_instances:
        g.scheduler.cancel(j)
        logger.info("job %s has been canceled", j)

    load_checkers(python_checker)


@main.command(help="Manually generate reports")
@click.option("--check-name", help="The check job's name")
@click.option("--check-id", help="The ID of one check, it's normally an int timestamp")
@click.option(
    "-r",
    "--result-path",
    type=click.Path(),
    default=None,
    help="Where to save the results",
)
def generate_reports(check_name, check_id, result_path):
    g.role = Role.REPORTER
    g.result_path = result_path
    logger.info(
        "Manually trigger generate report for job=%s, check_id=%s", check_name, check_id
    )
    generate_report(check_name, check_id)


@main.command(help="Admin web HTTP server")
@click.option("--host", default="127.0.0.1", help="The interface to bind to.")
@click.option("--port", default=8080, help="The port to bind to.")
@click.option("--connection-limit", "-c", default=1000, help="Server connection limit")
@click.option("--threads", "-t", default=64, help="Server threads")
@click.option(
    "-p",
    "--python-checker",
    type=click.Path(),
    default=None,
    help="Python checker script location",
)
@click.option(
    "-r",
    "--result-path",
    type=click.Path(),
    default=None,
    help="Where to save the results",
)
def admin(host, port, connection_limit, threads, python_checker, result_path):
    load_checkers(python_checker)
    g.result_path = result_path
    g.scheduler = Scheduler(
        queue=g.checker_queue, connection=g.checker_queue.connection
    )
    app = create_app()
    waitress.serve(
        app,
        host=host,
        port=port,
        connection_limit=connection_limit,
        threads=threads,
    )


def start_worker(queue):
    w = Worker(queue, connection=g.redis)
    w.work()
