from abc import ABC, abstractmethod
from typing import Any, Iterable
from src.core.domain.trainStation import TrainStationBroker

class ITrainStationRepository(ABC):

    @abstractmethod
    async def add_station(self, station: TrainStationBroker) -> Any | None:
        """
        create new train station
        """
    @abstractmethod
    async def get_by_city(self,city:str) -> Iterable[Any]:
        """
        returns all stations located in city

        """

    @abstractmethod
    async def get_by_id(self, station_id: int) -> Any | None:
        """
        get train station by id
        """

    @abstractmethod
    async def get_all(self) -> Iterable[Any]:
        """
        return a list of train stations
        """

    @abstractmethod
    async def delete_station(self, station_id: int) -> bool:
        """
        delete station by id
        """
