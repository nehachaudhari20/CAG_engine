from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class ExecutionState:
    """
    Shared state passed across the execution DAG.
    """
    context: Dict[str, Any] = field(default_factory=dict)
    history: List[Dict[str, Any]] = field(default_factory=list)

    def apply(self, updates: Dict[str, Any], node_id: str):
        """
        Apply step updates and record state transition.
        """
        self.context.update(updates)
        self.history.append({
            "node": node_id,
            "updates": updates
        })
