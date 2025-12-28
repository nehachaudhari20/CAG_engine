from dataclasses import dataclass
from typing import Callable
from cag_engine.schema.state import ExecutionState


@dataclass(frozen=True)
class ExecutionEdge:
    """
    Directed conditional transition between two nodes.
    """
    from_node: str
    to_node: str
    condition: Callable[[ExecutionState], bool]
    priority: int = 0
