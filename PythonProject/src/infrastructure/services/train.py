"""A module containing train service implementation."""

from typing import Iterable
from src.core.domain.train import TrainIn
from src.core.repositories.itrain import ITrainRepository
from src.infrastructure.dto.traindto import TrainDTO
from src.infrastructure.services.itrain import ITrainService


class TrainService(ITrainService):
    """A class implementing train service."""

    _repository: ITrainRepository

    def __init__(self, repository: ITrainRepository) -> None:
        """Initialize the train service."""
        self._repository = repository

    async def add_train(self, train: TrainIn) -> TrainDTO | None:
        """Add new train"""
        return await self._repository.add_train(train)

    async def get_by_id(self, train_id: int) -> TrainDTO | None:
        """Get train by id"""
        return await self._repository.get_by_id(train_id)

    async def get_all(self) -> Iterable[TrainDTO]:
        """Get all train"""
        return await self._repository.get_all()

    async def delete_train(self, train_id: int) -> bool:
        """Delete train"""
        return await self._repository.delete_train(train_id)
