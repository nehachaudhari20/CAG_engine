from cag_engine.schema.step import Step
from cag_engine.graph.node import ExecutionNode
from cag_engine.graph.edge import ExecutionEdge
from cag_engine.graph.graph import ExecutionGraph
from cag_engine.engine import CAGEngine
from cag_engine.schema.state import ExecutionContext

class IngestEventStep(Step):
    def run(self, state):
        return {
            "txn_id": "txn_123",
            "retry_count": state.get("retry_count", 0)
        }

class ExtractSignalsStep(Step):
    def run(self, state):
        return {
            "signals": ["timeout", "bank_delay"]
        }

class VerifyEvidenceStep(Step):
    def run(self, state):
        retry_count = state.get("retry_count", 0)

        # simulate confidence improving with retries
        confidence = 0.4 + (0.2 * retry_count)

        return {
            "confidence": confidence
        }

class RetryFetchStep(Step):
    def run(self, state):
        return {
            "retry_count": state.get("retry_count", 0) + 1
        }


class FinalizeStep(Step):
    def run(self, state):
        return {
            "final_decision": "BANK_TIMEOUT",
            "resolved": True
        }


nodes = {
    "ingest": ExecutionNode("ingest", IngestEventStep()),
    "extract": ExecutionNode("extract", ExtractSignalsStep()),
    "verify": ExecutionNode("verify", VerifyEvidenceStep()),
    "retry": ExecutionNode("retry", RetryFetchStep()),
    "finalize": ExecutionNode("finalize", FinalizeStep()),
}

edges = [
    ExecutionEdge("ingest", "extract", lambda s: True),
    ExecutionEdge("extract", "verify", lambda s: True),

    # branch based on confidence
    ExecutionEdge(
        "verify",
        "retry",
        lambda s: s.context.get("confidence", 0) < 0.6,
        priority=1
    ),
    ExecutionEdge(
        "verify",
        "finalize",
        lambda s: s.context.get("confidence", 0) >= 0.6,
        priority=0
    ),

    # retry loop
    ExecutionEdge(
        "retry",
        "verify",
        lambda s: s.context.get("retry_count", 0) < 3
    )
]

graph = ExecutionGraph(
    nodes=nodes,
    edges=edges,
    start_node="ingest"
)

engine = CAGEngine(graph)
context = engine.run(ExecutionContext())


print(context.state.context)
