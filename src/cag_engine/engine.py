from cag_engine.graph.graph import ExecutionGraph
from cag_engine.execution.executor import GraphExecutor
from cag_engine.execution.termination import TerminationPolicy
from cag_engine.schema.state import ExecutionContext


class CAGEngine:
    """
    Public entrypoint for executing control-flow graphs.
    """

    def __init__(
        self,
        graph: ExecutionGraph,
        termination_policy: TerminationPolicy | None = None
    ):
        self.graph = graph
        self.executor = GraphExecutor(
            graph=graph,
            termination_policy=termination_policy
        )

    def run(
        self,
        initial_context: ExecutionContext | None = None
    ) -> ExecutionContext:
        """
        Execute the graph from start node with an optional initial context.
        """
        context = initial_context or ExecutionContext()
        return self.executor.run(context)

    @staticmethod
    def summarize(context: ExecutionContext) -> dict:
        """
        Produce a concise execution summary from the trace.
        """
        events = context.trace.events

        return {
            "steps_executed": len(
                [e for e in events if e.event_type == "node_start"]
            ),
            "nodes_visited": [
                e.node_id for e in events if e.event_type == "node_start"
            ],
            "termination": next(
                (e.data for e in reversed(events)
                 if e.event_type == "termination"),
                None
            ),
            "final_state": dict(context.state.context)
        }
