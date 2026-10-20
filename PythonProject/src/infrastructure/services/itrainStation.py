"""A module containing train station service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable
from src.core.domain.trainStation import TrainStationBroker
from src.infrastructure.dto.trainStationdto import TrainStationDTO


class ITrainStationService(ABC):
    """An abstract class for train station service."""

    @abstractmethod
    async def add_station(self, station: TrainStationBroker) -> TrainStationDTO | None:
        """Add a new train station."""

    @abstractmethod
    async def get_by_id(self, station_id: int) -> TrainStationDTO | None:
        """Get a train station by its ID."""

    @abstractmethod
    async def get_all(self) -> Iterable[TrainStationDTO]:
        """Get all train stations."""

    @abstractmethod
    async def get_by_city(self, city:str) -> Iterable[TrainStationDTO]:
        """Get train stations by city."""

    @abstractmethod
    async def delete_station(self, station_id: int) -> bool:
        """Delete a train station by its ID."""
