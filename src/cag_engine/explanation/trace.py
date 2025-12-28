from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from datetime import datetime


@dataclass(frozen=True)
class TraceEvent:
    """
    Immutable record of a single execution event.
    """
    event_type: str                # "node_start", "node_end", "edge_taken", "termination"
    node_id: Optional[str]
    data: Dict[str, Any]
    timestamp: datetime


class ExecutionTrace:
    """
    Append-only execution timeline.
    """

    def __init__(self):
        self._events: List[TraceEvent] = []

    def record(
        self,
        event_type: str,
        node_id: Optional[str],
        data: Dict[str, Any]
    ):
        self._events.append(
            TraceEvent(
                event_type=event_type,
                node_id=node_id,
                data=data,
                timestamp=datetime.utcnow()
            )
        )

    @property
    def events(self) -> List[TraceEvent]:
        return list(self._events)

    def to_dict(self) -> List[Dict[str, Any]]:
        """
        Serialize trace for logging / storage / replay.
        """
        return [
            {
                "event_type": e.event_type,
                "node_id": e.node_id,
                "data": e.data,
                "timestamp": e.timestamp.isoformat()
            }
            for e in self._events
        ]
