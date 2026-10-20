from abc import ABC, abstractmethod
from typing import Any, Iterable
from src.core.domain.train import TrainIn

class ITrainRepository(ABC):

    @abstractmethod
    async def add_train(self, train: TrainIn) -> Any | None:
        """
        create a new train
        """

    @abstractmethod
    async def get_by_id(self, train_id: int) -> Any | None:
        """
        get train by id
        """

    @abstractmethod
    async def get_all(self) -> Iterable[Any]:
        """
        returns list of all trains
        """

    @abstractmethod
    async def delete_train(self, train_id: int) -> bool:
        """
        delete train by id
        """
