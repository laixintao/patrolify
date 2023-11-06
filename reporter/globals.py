from dataclasses import dataclass, field
from typing import Dict, Union


@dataclass
class Global:
    target_checkers: Dict = field(default_factory=dict)
    checker_queue = None
    scheduler = None
    role: Union[None, str] = None


g = Global()
