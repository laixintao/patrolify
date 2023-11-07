import time
import logging
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


class TimeTriggerTarget(Target):
    def __init__(self) -> None:
        super().__init__()
        self.trigger_timestamp = time.time
