import importlib
import importlib.util
import logging
import os

import click
from redis import Redis
from rq import Queue, Worker

from rq_scheduler import Scheduler

from .globals import Role, g


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
    logger.info("------ reporter ------")


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
def main(verbose, log_to, redis_url):
    log_level = LOG_LEVEL[verbose]
    setup_log(log_to is not None, log_level, log_to)
    g.redis = Redis.from_url(redis_url)
    g.checker_queue = Queue("checker", connection=g.redis)


@main.command()
@click.option(
    "-p",
    "--python-checker",
    type=click.Path(),
    default=None,
    help="Python checker script location",
)
def worker(python_checker):
    g.role = Role.WORKER
    load_checkers(python_checker)
    start_worker()


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


def load_checkers(path):
    for root, _, files in os.walk(path):
        for file in files:
            abs_path = os.path.join(root, file)
            if not file.endswith(".py"):
                logger.debug("%s is not ending with .py, ignore...", abs_path)
                continue
            logger.info("import python file: %s", abs_path)

            module_name = abs_path[:-3].replace("/", ".")
            importlib.import_module(module_name)
    logger.info("Loading checkers done: %s", g.target_checkers)


def start_worker():
    w = Worker([g.checker_queue], connection=g.redis)
    w.work()
