from cag_engine.graph.graph import ExecutionGraph


class SubGraph:
    """
    A reusable execution graph fragment.
    """

    def __init__(self, graph: ExecutionGraph):
        self.graph = graph

    def entry(self) -> str:
        return self.graph.start_node

    def nodes(self):
        return self.graph.nodes

    def edges(self):
        return self.graph.edges
