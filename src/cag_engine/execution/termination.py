from dataclasses import dataclass
from typing import Optional


@dataclass
class TerminationPolicy:
    """
    Defines safety limits for execution.
    """
    max_steps: int = 50
    max_retries: int = 5


@dataclass
class TerminationResult:
    terminated: bool
    reason: Optional[str] = None
    