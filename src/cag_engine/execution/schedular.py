from cag_engine.schema.state import ExecutionState
from cag_engine.execution.termination import TerminationPolicy, TerminationResult


class SafetyScheduler:
    """
    Enforces execution safety constraints.
    """

    def __init__(self, policy: TerminationPolicy):
        self.policy = policy

    def check(
        self,
        step_count: int,
        state: ExecutionState
    ) -> TerminationResult:

        if step_count >= self.policy.max_steps:
            return TerminationResult(
                terminated=True,
                reason="max_steps_exceeded"
            )

        if state.context.get("retry_count", 0) > self.policy.max_retries:
            return TerminationResult(
                terminated=True,
                reason="max_retries_exceeded"
            )

        return TerminationResult(terminated=False)
