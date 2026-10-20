"""A module containing connection service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable


from src.core.domain.connection import ConnectionIn
from src.infrastructure.dto.connectiondto import ConnectionDTO


class IConnectionService(ABC):
    """An abstract class for connection service."""

    @abstractmethod
    async def create_connection(self, connection: ConnectionIn) -> ConnectionDTO | None:
        """Create a new train connection."""

    @abstractmethod
    async def search_by_city(self, start_city: str, end_city: str) -> Iterable[ConnectionDTO]:
        pass

    @abstractmethod
    async def get_by_id(self, connection_id: int) -> ConnectionDTO | None:
        """Get a connection by its ID."""

    @abstractmethod
    async def get_all_connections(self) -> Iterable[ConnectionDTO]:
        """Get all train connections."""

    @abstractmethod
    async def search_connections(self, departure_station_id: int, arrival_station_id: int) -> Iterable[ConnectionDTO]:
        """Search connections between two stations."""
