from dataclasses import dataclass, field
from enum import Enum
import threading
from typing import Dict


class Role(Enum):
    SCHEDULER = "sheduler"
    PLANNER = "planner"
    WORKER = "worker"


@dataclass
class Global:
    target_checkers: Dict = field(default_factory=dict)
    triggers: Dict = field(default_factory=dict)
    checker_queue = None
    scheduler = None
    role: Role = Role.WORKER
    redis = None
    result_path = None


g = Global()

threadlocal = threading.local()
