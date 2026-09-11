from abc import ABC, abstractmethod
from uuid import UUID

from sentinel.models.evaluation import Evaluation


class EvaluationStore(ABC):
    @abstractmethod
    async def save(self, evaluation: Evaluation) -> None:
        """Persist an evaluation."""
        raise NotImplementedError

    @abstractmethod
    async def get(
        self,
        evaluation_id: UUID,
    ) -> Evaluation | None:
        """Return an evaluation by ID."""
        raise NotImplementedError


class InMemoryEvaluationStore(EvaluationStore):
    def __init__(self) -> None:
        self._evaluations: dict[UUID, Evaluation] = {}

    async def save(
        self,
        evaluation: Evaluation,
    ) -> None:
        self._evaluations[evaluation.evaluation_id] = evaluation

    async def get(
        self,
        evaluation_id: UUID,
    ) -> Evaluation | None:
        return self._evaluations.get(evaluation_id)