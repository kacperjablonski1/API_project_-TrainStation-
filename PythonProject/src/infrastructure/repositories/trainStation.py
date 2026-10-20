from typing import Any, Iterable

from src.core.domain.trainStation import TrainStationBroker, TrainStation
from src.core.repositories.itrainStation import ITrainStationRepository
from src.db import database, trainStation_table


class TrainStationRepository(ITrainStationRepository):
    async def add_station(self, station: TrainStationBroker) -> TrainStation | None:
        """Adds a new train station"""

        query = trainStation_table.insert().values(**station.model_dump())
        new_station_id = await database.execute(query)

        return await self.get_by_id(new_station_id)

    async def get_by_id(self, station_id: int) -> TrainStation | None:
        """retrieves a train station by id"""

        query = trainStation_table.select().where(trainStation_table.c.id == station_id)
        station = await database.fetch_one(query)

        if station:
            return TrainStation(**station)
        return None

    async def get_by_city(self, city: str) -> Iterable[TrainStation]:
        """returns all stations by city"""
        query = trainStation_table.select().where(trainStation_table.c.city == city)
        stations = await database.fetch_all(query)
        return [TrainStation(**station) for station in stations]

    async def get_all(self) -> Iterable[TrainStation]:
        """returns all stations"""

        query = trainStation_table.select()
        stations = await database.fetch_all(query)

        return [TrainStation(**station) for station in stations]

    async def delete_station(self, station_id: int) -> bool:
        """delete station by id"""

        query = trainStation_table.delete().where(trainStation_table.c.id == station_id)
        result = await database.execute(query)

        return bool(result)
