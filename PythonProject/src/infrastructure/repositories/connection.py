from typing import Any, Iterable

from src.core.domain.connection import ConnectionIn
from src.core.repositories.iconnection import IConnectionRepository
from src.db import database, connection_table


class ConnectionRepository(IConnectionRepository):

    async def create_connection(self, connection: ConnectionIn) -> Any | None:
        """
        creates a new connection and returns
        """
        query = connection_table.insert().values(**connection.model_dump())
        new_connection_id = await database.execute(query)
        return await self.get_by_id(new_connection_id)

    async def get_by_id(self, connection_id: int) -> Any | None:
        """
        retrives a connection by id
        """
        query = connection_table.select().where(connection_table.c.id == connection_id)
        connection = await database.fetch_one(query)
        return connection

    async def get_all_connections(self) -> Iterable[Any]:
        """
        retrives all connections
        """
        query = connection_table.select()
        connections = await database.fetch_all(query)
        return connections

    async def search_connections(
        self, departure_station_id: int, arrival_station_id: int) -> Iterable[Any]:
        """
        search for connections between two stations
        """
        query = (
            connection_table.select()
            .where(connection_table.c.departure_station_id == departure_station_id)
            .where(connection_table.c.arrival_station_id == arrival_station_id)
        )
        results = await database.fetch_all(query)
        return results
