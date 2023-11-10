from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import threading
from typing import Dict


class Role(Enum):
    SCHEDULER = "sheduler"
    PLANNER = "planner"
    WORKER = "worker"
    REPORTER = "reporter"


@dataclass
class Global:
    target_checkers: Dict = field(default_factory=dict)
    triggers: Dict = field(default_factory=dict)
    checker_queue = None
    scheduler = None
    role: Role = Role.WORKER
    redis = None
    result_path = None

    def result_dir(self, check_name, check_id):
        return Path(self.result_path) / check_name / check_id


g = Global()

threadlocal = threading.local()
