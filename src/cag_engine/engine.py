from cag_engine.graph.graph import ExecutionGraph
from cag_engine.execution.executor import GraphExecutor
from cag_engine.schema.state import ExecutionContext


class CAGEngine:
    """
    Public interface for running execution graphs.
    """

    def __init__(self, graph: ExecutionGraph):
        self.executor = GraphExecutor(graph)

    def run(self, initial_context: ExecutionContext | None = None) -> ExecutionContext:
        context = initial_context or ExecutionContext()
        return self.executor.run(context)
