from datetime import datetime
import logging
import time
import uuid

from .globals import threadlocal


logger = logging.getLogger(__name__)


class Target:
    def __init__(self) -> None:
        self.check_id = threadlocal.check_id
        self.check_name = threadlocal.check_name

        self.job_id = str(uuid.uuid4())
        if hasattr(threadlocal, "current_target"):
            self.parent_target = threadlocal.current_target.job_id
        else:
            self.parent_target = None

    @property
    def scheduled_count_key(self):
        return f"patrolify:{self.check_name}:{self.check_id}:scheduled"

    @property
    def finished_count_key(self):
        return f"patrolify:{self.check_name}:{self.check_id}:finished"

    @property
    def started_time_key(self):
        return f"patrolify:{self.check_name}:{self.check_id}:started_timestamp"


class TimeTriggerTarget(Target):
    def __init__(self) -> None:
        super().__init__()
        self.trigger_timestamp = time.time()

    def __str__(self):
        datetime_obj = datetime.fromtimestamp(self.trigger_timestamp)
        formatted_string = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
        return f"Trigger at {formatted_string}"
