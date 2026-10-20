"""A module containing train station service implementation."""

from typing import Iterable
from src.core.domain.trainStation import TrainStationBroker
from src.core.repositories.itrainStation import ITrainStationRepository
from src.infrastructure.dto.trainStationdto import TrainStationDTO
from src.infrastructure.services.itrainStation import ITrainStationService


class TrainStationService(ITrainStationService):
    """A class implementing train station service."""

    _repository: ITrainStationRepository

    def __init__(self, repository: ITrainStationRepository) -> None:
        """Initialize train station service."""
        self._repository = repository

    async def add_station(self, station: TrainStationBroker) -> TrainStationDTO | None:
        """Add new train station"""
        return await self._repository.add_station(station)

    async def get_by_id(self, station_id: int) -> TrainStationDTO | None:
        """Get train station by id"""
        return await self._repository.get_by_id(station_id)

    async def get_all(self) -> Iterable[TrainStationDTO]:
        """Get all train stations"""
        return await self._repository.get_all()

    async def get_by_city(self, city:str) -> Iterable[TrainStationDTO]:
        """Get train station by city"""
        stations = await self._repository.get_by_city(city)
        return [TrainStationDTO.model_validate(s) for s in stations]

    async def delete_station(self, station_id: int) -> bool:
        """Delete train station"""
        return await self._repository.delete_station(station_id)
