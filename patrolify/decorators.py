from datetime import datetime
import logging

from patrolify.exceptions import UsageError

from .globals import Role, g
from .queue_jobs import trigger_target


logger = logging.getLogger(__name__)


def check(target_cls):
    def wrapper(func):
        logger.info("Register checker for target: %s", target_cls)
        # register the target checker
        g.target_checkers[target_cls] = func
        return func

    return wrapper


def trigger(interval_seconds=None, cron_string=None):
    if not interval_seconds and not cron_string:
        raise UsageError("Must set interval_seconds or cron_string")

    scheduler = g.scheduler

    def wrapper(func):
        funcname = f"{func.__module__}.{func.__name__}"
        if g.role != Role.PLANNER:
            g.triggers[funcname] = func
            logger.info("Regisgered a trigger: %s", funcname)
            return func
        logger.info(
            "Schedule jobs func %s for interval_seconds=%s, cron_string=%s",
            funcname,
            interval_seconds,
            cron_string,
        )
        if interval_seconds:
            scheduler.schedule(
                scheduled_time=datetime.utcnow(),
                func=trigger_target,
                interval=interval_seconds,
                args=[funcname],
            )
        else:
            scheduler.cron(
                cron_string,
                func=trigger_target,
                args=[funcname],
            )
        # TODO schedule jobs
        return func

    return wrapper
