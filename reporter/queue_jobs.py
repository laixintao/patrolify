import logging
import types

from .globals import g

logger = logging.getLogger(__name__)


def check_target(target):
    logger.info("check on target=%s", target)
    checker_func = get_checker(target)
    result = checker_func(target)
    return paorcess_result(result)


def paorcess_result(result):
    if isinstance(result, tuple):
        return result
    if isinstance(result, types.GeneratorType):
        for target in result:
            queue_target(target)


def trigger_target(funcname):
    logger.info("Start running the trigger function: %s", funcname)
    trigger = g.triggers[funcname]
    result = trigger()
    return paorcess_result(result)


def get_checker(target):
    target_type = target.__class__
    checker_func = g.target_checkers[target_type]
    return checker_func


def queue_target(target):
    g.checker_queue.enqueue(check_target, target)
