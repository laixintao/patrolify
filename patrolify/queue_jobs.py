import logging
import time
import types
from patrolify.consts import GLOBAL_TTL_SECONDS

from patrolify.target import TimeTriggerTarget

from .globals import g, threadlocal
from .reports import generate_report, store_check_result

logger = logging.getLogger(__name__)


def check_target(target):
    logger.info("check on target=%s", target)
    restore_thread_local(target)

    checker_func = get_checker(target)
    result = checker_func(target)
    return process_result(result, target)


def trigger_target(funcname):
    threadlocal.check_id = str(int(time.time()))
    threadlocal.check_name = funcname

    logger.info("Start running the trigger function: %s", funcname)
    target = TimeTriggerTarget()

    redis = g.redis
    exat = int(time.time() + GLOBAL_TTL_SECONDS)
    redis.set(target.scheduled_count_key, 1, exat=exat)
    redis.set(target.finished_count_key, 0, exat=exat)
    redis.set(target.started_time_key, time.time(), exat=exat)

    threadlocal.current_target = target
    trigger = g.triggers[funcname]
    result = trigger(target)

    process_result(result, target)


def process_result(result, target):
    if isinstance(result, tuple):
        g.reporter_queue.enqueue(
            store_check_result,
            result,
            str(target),
            target.check_name,
            target.check_id,
            target.job_id,
            target.parent_target,
        )

    if isinstance(result, types.GeneratorType):
        try:
            while True:
                t = next(result)
                queue_target(t)
        except StopIteration as e:
            check_result = e.value
            g.reporter_queue.enqueue(
                store_check_result,
                check_result,
                str(target),
                target.check_name,
                target.check_id,
                target.job_id,
                target.parent_target,
            )

    incr_task_count_and_check_finsihed(target)


def incr_task_count_and_check_finsihed(target):
    redis = g.redis

    finished_count = redis.incr(target.finished_count_key)
    scheduled_count = int(redis.get(target.scheduled_count_key))

    if finished_count == scheduled_count:
        logger.info(
            "all tasks has been finsiehd, %s=%d, %s=%d",
            target.scheduled_count_key,
            scheduled_count,
            target.finished_count_key,
            finished_count,
        )
        g.reporter_queue.enqueue(generate_report, target.check_name, target.check_id)


def get_checker(target):
    target_type = target.__class__
    checker_func = g.target_checkers[target_type]
    return checker_func


def queue_target(target):
    redis = g.redis
    redis.incr(target.scheduled_count_key)
    g.checker_queue.enqueue(check_target, target)


def restore_thread_local(target):
    threadlocal.check_id = target.check_id
    threadlocal.check_name = target.check_name
    threadlocal.current_target = target
