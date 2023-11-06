import logging
from reporter.exceptions import UsageError
from .globals import g, Role


logger = logging.getLogger(__name__)


def check(target_cls):
    def wrapper(func):
        target_type_name = target_cls.__module__ + "." + target_cls.__qualname__
        logger.info("Register checker for target: %s", target_type_name)
        # register the target checker
        g.target_checkers[target_type_name] = func
        return func

    return wrapper


def trigger(interval_seconds=None, cron_string=None):
    if not interval_seconds and not cron_string:
        raise UsageError("Must set interval_seconds or cron_string")

    scheduler = g.scheduler

    def wrapper(func):
        if g.role != Role.PLANNER:
            return func
        if interval_seconds:
            scheduler.schedule(func=func, interval=interval_seconds)
        else:
            scheduler.schedule(
                cron_string,
                func=func,
            )
        # TODO schedule jobs
        return func

    return wrapper
