"""A module containing connection service implementation."""
from  fastapi import HTTPException
from typing import Iterable


from src.core.domain.connection import ConnectionIn
from src.core.repositories.iconnection import IConnectionRepository
from src.core.repositories.itrainStation import ITrainStationRepository
from src.infrastructure.dto.connectiondto import ConnectionDTO
from src.infrastructure.services.iconnection import IConnectionService


class ConnectionService(IConnectionService):
    """A class implementing connection service."""

    _repository: IConnectionRepository

    def __init__(self, repository: IConnectionRepository, station_repository:ITrainStationRepository) -> None:
        """Initialize the connection service."""
        self._repository = repository
        self._station_repository = station_repository

    async def create_connection(self, connection: ConnectionIn) -> ConnectionDTO | None:
        """Creates a new connection."""
        if new_conn :=await self._repository.create_connection(connection):
            return ConnectionDTO.model_validate(new_conn)
        return None

    async def get_by_id(self, connection_id: int) -> ConnectionDTO | None:
        """Gets a connection by id."""
        if conn := await self._repository.get_by_id(connection_id):
            return ConnectionDTO.model_validate(conn)
        return None

    async def search_by_city(self, start_city: str, end_city: str) -> Iterable[ConnectionDTO]:
        """Searches for connections by city."""
        start_stations = await self._station_repository.get_by_city(start_city)
        if not start_stations:
            return []

        end_stations = await self._station_repository.get_by_city(end_city)
        if not end_stations:
            return []

        results = []

        for s in start_stations:
            for e in end_stations:
                connections = await self._repository.search_connections(
                    departure_station_id=s.id,
                    arrival_station_id=e.id,
                )
                for c in connections:
                    results.append(ConnectionDTO.model_validate(c))
        return results

    async def get_all_connections(self) -> Iterable[ConnectionDTO]:
        """Gets all connections."""
        conns = await self._repository.get_all_connections()
        return [ConnectionDTO.model_validate(c) for c in conns]

    async def search_connections(self, departure_station_id: int, arrival_station_id: int) -> Iterable[ConnectionDTO]:
        """Searches for connections by station."""
        conns = await self._repository.search_connections(departure_station_id, arrival_station_id)
        return [ConnectionDTO.model_validate(c) for c in conns]
