from abc import ABC, abstractmethod
from typing import Any, Iterable

from src.core.domain.connection import ConnectionIn

class IConnectionRepository(ABC):

    @abstractmethod
    async def create_connection(self, connection: ConnectionIn) -> Any | None:
        """
        create a new train connection
        """

    @abstractmethod
    async def get_by_id(self, connection_id: int) -> Any | None:
        """
        get connection by id
        """

    @abstractmethod
    async def get_all_connections(self) -> Iterable[Any]:
        """
        return all connections
        """

    @abstractmethod
    async def search_connections(self, departure_station_id: int, arrival_station_id: int) -> Iterable[Any]:
        """
        Search for conection between two stations
        """
