"""A module containing train service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable
from src.core.domain.train import TrainIn
from src.infrastructure.dto.traindto import TrainDTO


class ITrainService(ABC):
    """An abstract class for train service."""

    @abstractmethod
    async def add_train(self, train: TrainIn) -> TrainDTO | None:
        """Add a new train."""

    @abstractmethod
    async def get_by_id(self, train_id: int) -> TrainDTO | None:
        """Get a train by its ID."""

    @abstractmethod
    async def get_all(self) -> Iterable[TrainDTO]:
        """Get all trains."""

    @abstractmethod
    async def delete_train(self, train_id: int) -> bool:
        """Delete a train by its ID."""
