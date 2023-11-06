from dataclasses import dataclass, field
from enum import Enum
from typing import Dict


class Role(Enum):
    SCHEDULER = "sheduler"
    PLANNER = "planner"
    WORKER = "worker"

@dataclass
class Global:
    target_checkers: Dict = field(default_factory=dict)
    checker_queue = None
    scheduler = None
    role: Role = Role.WORKER
    redis = None


g = Global()
