import json
import logging
import time
import types
from reporter.consts import GLOBAL_TTL_SECONDS

from reporter.target import TimeTriggerTarget

from .globals import g, threadlocal

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
        store_check_result(result, target)

    if isinstance(result, types.GeneratorType):
        try:
            while True:
                t = next(result)
                queue_target(t)
        except StopIteration as e:
            check_result = e.value
            store_check_result(check_result, target)

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


def store_check_result(result, target):
    data = {
        "job_id": target.job_id,
        "target": str(target),
        "parent_target_id": target.parent_target,
        "run_success": None,
        "check_pass": None,
        "reason": None,
    }

    if result is None:
        pass
    elif isinstance(result, tuple):
        boolresult, reason = result

        data.update(
            {
                "run_success": True,
                "check_pass": boolresult,
                "reason": reason,
            }
        )

    check_name = target.check_name
    check_id = target.check_id
    result_dir = g.result_path / check_name / check_id
    result_dir.mkdir(parents=True, exist_ok=True)
    with open(str(result_dir / target.job_id) + ".json", "w") as f:
        json.dump(data, f)
        logger.info("Job result has been saved to %s", f)
