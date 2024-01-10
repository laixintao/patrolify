import json
import logging
from flask import Blueprint, jsonify
from reporter.globals import g
from reporter.consts import RESULT_FILE_NAME
from reporter.reports import get_latest_check_ids

logger = logging.getLogger(__name__)
admin_api_blueprint = Blueprint("admin_api", __name__, url_prefix="/api/v1")


@admin_api_blueprint.route("/triggers")
def triggers_list():
    checker_queue = g.checker_queue
    scheduled_jobs = checker_queue.scheduled_job_registry

    list_of_job_instances = g.scheduler.get_jobs()

    scheduled_triggers = list(j.args[0] for j in list_of_job_instances)

    checkers = []
    for trigger in scheduled_triggers:
        report_path = get_latest_report_dir(trigger)
        if not report_path:
            checkers.append({
                "name": trigger,
                "latest_report_dir": None,
                "latest_report_timestamp": None,
                "report": None,
            })
            continue
        checkers.append({
            "name": trigger,
            "latest_report_dir": str(report_path),
            "latest_report_timestamp": str(report_path.name),
            "report": get_report_by_path(report_path),
        })

    return jsonify({
        "scheduled_jobs_count": scheduled_jobs.count,
        "checkers": checkers,
    })


@admin_api_blueprint.route("/checker/<name>")
def checker_detail(name):
    latest_check_ids = [str(x).strip() for x in get_latest_check_ids(name)]
    return jsonify({"latest_check_ids": latest_check_ids})


def get_latest_report_dir(trigger_name):
    report_dir = g.report_base_dir(trigger_name)

    if not report_dir.exists():
        return None
    report_dirs = sorted(report_dir.iterdir())
    logger.info("year list: %s", report_dirs)

    report_dir = report_dirs[-1]
    report_dirs = sorted(report_dir.iterdir())
    logger.info("month list: %s", report_dirs)

    report_dir = report_dirs[-1]
    report_dirs = sorted(report_dir.iterdir())
    logger.info("day list: %s", report_dirs)

    report_dir = report_dirs[-1]
    report_dirs = sorted(report_dir.iterdir())
    logger.info("hour list: %s", report_dirs)

    report_dir = report_dirs[-1]
    report_dirs = sorted(report_dir.iterdir())
    logger.info("ts list: %s", report_dirs)

    report_dir = report_dirs[-1]
    logger.info("latest report dir is: %s", report_dir)

    return report_dir


def get_report_by_path(path):
    with open(path / RESULT_FILE_NAME) as f:
        return json.load(f)
