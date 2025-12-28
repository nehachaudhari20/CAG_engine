from dataclasses import dataclass
from cag_engine.schema.step import Step


@dataclass(frozen=True)
class ExecutionNode:
    """
    A node represents one executable step in the DAG.
    """
    node_id: str
    step: Step
