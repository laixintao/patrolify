import logging
from flask import Blueprint, jsonify
from reporter.globals import g

logger = logging.getLogger(__name__)
admin_api_blueprint = Blueprint("admin_api", __name__, url_prefix="/api/v1")


@admin_api_blueprint.route("/triggers")
def triggers_list():
    checker_queue = g.checker_queue
    scheduled_jobs = checker_queue.scheduled_job_registry

    triggers = list(g.triggers.keys())
    list_of_job_instances = g.scheduler.get_jobs()

    return jsonify({
        "scheduled_jobs_count": scheduled_jobs.count,
        "scheduler_scheduled_jobs": [
            {
                "job_id": j.id,
                "job_func_name": j.func_name,
                "args": j.args,
                "kwargs": j.kwargs,
            }
            for j in list_of_job_instances
        ],
        "triggers": triggers,
    })
