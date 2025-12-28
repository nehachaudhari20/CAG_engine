from typing import Dict, List
from cag_engine.graph.node import ExecutionNode
from cag_engine.graph.edge import ExecutionEdge


class ExecutionGraph:
    """
    Control-flow DAG defining possible execution paths.
    """

    def __init__(
        self,
        nodes: Dict[str, ExecutionNode],
        edges: List[ExecutionEdge],
        start_node: str
    ):
        self.nodes = nodes
        self.edges = edges
        self.start_node = start_node

        self._validate()

    def _validate(self):
        if self.start_node not in self.nodes:
            raise ValueError(f"Start node '{self.start_node}' not found")

        for edge in self.edges:
            if edge.from_node not in self.nodes:
                raise ValueError(f"Invalid edge source: {edge.from_node}")
            if edge.to_node not in self.nodes:
                raise ValueError(f"Invalid edge target: {edge.to_node}")

    def outgoing_edges(self, node_id: str) -> List[ExecutionEdge]:
        """
        Return outgoing edges sorted by priority (high → low).
        """
        return sorted(
            [e for e in self.edges if e.from_node == node_id],
            key=lambda e: e.priority,
            reverse=True
        )
