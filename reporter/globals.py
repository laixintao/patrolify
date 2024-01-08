from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import threading
from typing import Callable, Dict


class Role(Enum):
    SCHEDULER = "sheduler"
    PLANNER = "planner"
    WORKER = "worker"
    REPORTER = "reporter"


@dataclass
class Global:
    target_checkers: Dict = field(default_factory=dict)
    triggers: Dict[str, Callable] = field(default_factory=dict)
    checker_queue = None
    reporter_queue = None
    scheduler = None
    role: Role = Role.WORKER
    redis = None
    result_path = None

    def result_dir(self, check_name, check_id):
        """save jobs result"""
        return Path(self.result_path) / check_name / "results" / check_id

    def report_dir(self, check_name, check_id):
        """save a check's result, when all jobs are finished, the result will
        be moved from ``result_dir`` to ``report_dir``
        """
        # year, month, day, hour
        time_path = datetime.utcfromtimestamp(int(check_id)).strftime("%Y/%m/%d/%H")
        return Path(self.result_path) / check_name / "reports" / time_path / check_id


g = Global()

threadlocal = threading.local()
