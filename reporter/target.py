import time
import uuid
from .globals import threadlocal


class Target:
    def __init__(self) -> None:
        self.check_id = threadlocal.check_id
        self.check_name = threadlocal.check_name
        self.job_id = str(uuid.uuid4())


class TimeTriggerTarget(Target):
    def __init__(self) -> None:
        super().__init__()
        self.trigger_timestamp = time.time
