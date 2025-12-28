from abc import ABC, abstractmethod
from typing import Dict, Any


class Step(ABC):
    """
    A Step performs a single atomic action.
    """

    @abstractmethod
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the step and return partial state updates.
        Must not mutate state directly.
        """
        raise NotImplementedError
