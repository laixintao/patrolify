import json
import logging
from pathlib import Path
import threading
import time
import types

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
    trigger = g.triggers[funcname]
    target = TimeTriggerTarget()
    result = trigger(target)
    return process_result(result, target)


def process_result(result, target):
    if isinstance(result, tuple):
        store_check_result(result, target)
    if isinstance(result, types.GeneratorType):
        for target in result:
            queue_target(target)


def get_checker(target):
    target_type = target.__class__
    checker_func = g.target_checkers[target_type]
    return checker_func


def queue_target(target):
    g.checker_queue.enqueue(check_target, target)


def restore_thread_local(target):
    threadlocal.check_id = target.check_id
    threadlocal.check_name = target.check_name


def store_check_result(result, target):
    if isinstance(result, tuple):
        boolresult, reason = result
        check_name = target.check_name
        check_id = target.check_id

        result_dir = g.result_path / check_name / check_id
        result_dir.mkdir(parents=True, exist_ok=True)

        data = {
            "run_success": True,
            "check_pass": boolresult,
            "reason": reason,
            "job_id": target.job_id,
            "target": str(target),
        }

        with open(str(result_dir / target.job_id) + ".json", "w") as f:
            json.dump(data, f)
            logger.info("Job result has been saved to %s", f)
