from typing import Any, Iterable

from src.core.domain.train import TrainIn
from src.core.repositories.itrain import ITrainRepository
from src.db import database, train_table


class TrainRepository(ITrainRepository):

    async def add_train(self, train: TrainIn) -> Any | None:
        """adds a new train"""

        query = train_table.insert().values(**train.model_dump())
        new_train_id = await database.execute(query)

        return await self.get_by_id(new_train_id)

    async def get_by_id(self, train_id: int) -> Any | None:
        """Retrieves a train by id"""

        query = (
            train_table
            .select()
            .where(train_table.c.id == train_id)
        )
        train = await database.fetch_one(query)

        return train

    async def get_all(self) -> Iterable[Any]:
        """returns all trains"""

        query = train_table.select()
        trains = await database.fetch_all(query)

        return trains

    async def delete_train(self, train_id: int) -> bool:
        """deletes a train"""

        query = (
            train_table
            .delete()
            .where(train_table.c.id == train_id)
        )
        result = await database.execute(query)

        return bool(result)
