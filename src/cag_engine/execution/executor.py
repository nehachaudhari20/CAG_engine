from cag_engine.graph.graph import ExecutionGraph
from cag_engine.schema.state import ExecutionContext
from cag_engine.execution.termination import TerminationPolicy
from cag_engine.execution.schedular import SafetyScheduler


class GraphExecutor:
    """
    Deterministic executor with safety controls.
    """

    def __init__(
        self,
        graph: ExecutionGraph,
        termination_policy: TerminationPolicy | None = None
    ):
        self.graph = graph
        self.policy = termination_policy or TerminationPolicy()
        self.scheduler = SafetyScheduler(self.policy)

    def run(self, context: ExecutionContext) -> ExecutionContext:
        current_node_id = self.graph.start_node
        step_count = 0

        while True:
            # --- SAFETY CHECK ---
            result = self.scheduler.check(step_count, context.state)
            if result.terminated:
                context.trace.record(
                    event_type="termination",
                    node_id=current_node_id,
                    data={"reason": result.reason}
                )
                break

            node = self.graph.nodes[current_node_id]

            # --- TRACE: node start ---
            context.trace.record(
                event_type="node_start",
                node_id=current_node_id,
                data={"step": step_count}
            )

            # --- EXECUTE STEP ---
            updates = node.step.run(context.state.context)

            # --- APPLY STATE ---
            context.state.apply(updates, node_id=current_node_id)

            # --- TRACE: node end ---
            context.trace.record(
                event_type="node_end",
                node_id=current_node_id,
                data={"updates": updates}
            )

            step_count += 1

            # --- EDGE EVALUATION ---
            next_node_id = None
            for edge in self.graph.outgoing_edges(current_node_id):
                if edge.condition(context.state):
                    next_node_id = edge.to_node
                    context.trace.record(
                        event_type="edge_taken",
                        node_id=current_node_id,
                        data={
                            "to": edge.to_node,
                            "priority": edge.priority
                        }
                    )
                    break

            # --- TERMINATION (no valid transition) ---
            if next_node_id is None:
                context.trace.record(
                    event_type="termination",
                    node_id=current_node_id,
                    data={"reason": "no_valid_outgoing_edge"}
                )
                break

            current_node_id = next_node_id

        return context
