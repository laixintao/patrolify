import importlib
import importlib.util
import logging
import os
import types

from redis import Redis

import click
from rq import Queue, Worker

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
    load_checkers(python_checker)
    g.role = Role.WORKER
    start_worker()


def load_checkers(path):
    for root, _, files in os.walk(path):
        for file in files:
            abs_path = os.path.join(root, file)
            if not file.endswith(".py"):
                logger.debug("%s is not ending with .py, ignore...", abs_path)
                continue
            logger.info("import python file: %s", abs_path)

            module_name = abs_path[:-3].replace("/", ".")
            spec = importlib.util.spec_from_file_location(module_name, abs_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
    logger.info("Loading checkers done: %s", g.target_checkers)


def start_worker():
    w = Worker([g.checker_queue], connection=g.redis)
    w.work()


def check_target(target):
    checker_func = get_checker(target)
    result = checker_func()

    if isinstance(result, tuple):
        return result
    if isinstance(result, types.GeneratorType):
        for target in result:
            queue_target(target)


def get_checker(target):
    target_type = target.__class__.__qualname__
    checker_func = g.target_checkers[target_type]
    return checker_func


def queue_target(target):
    g.checker_queue.enqueue(check_target, target)
