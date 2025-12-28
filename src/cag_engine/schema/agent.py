from dataclasses import dataclass
from typing import Dict, Any


@dataclass(frozen=True)
class AgentSpec:
    """
    Identifies the agent that owns an execution graph.
    No behavior lives here.
    """
    agent_id: str
    description: str
    metadata: Dict[str, Any]
