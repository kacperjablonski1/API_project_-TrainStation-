"""A repository for ticket entity."""

from typing import Any, Iterable

from src.core.domain.ticket import TicketIn
from src.core.repositories.iticket import ITicketRepository
from src.db import database, ticket_table
from uuid import UUID

class TicketRepository(ITicketRepository):

    async def add_ticket(self, ticket: TicketIn) -> Any | None:
        """Adds a new ticket"""

        query = ticket_table.insert().values(**ticket.model_dump())
        new_ticket_id = await database.execute(query)

        return await self.get_by_id(new_ticket_id)

    async def get_by_id(self, ticket_id: int) -> Any | None:
        """retrieves a ticket by id"""

        query = (
            ticket_table
            .select()
            .where(ticket_table.c.id == ticket_id)
        )
        ticket = await database.fetch_one(query)

        return ticket

    async def get_all(self) -> Iterable[Any]:
        """returns all tickets"""

        query = ticket_table.select()
        tickets = await database.fetch_all(query)

        return tickets

    async def delete_ticket(self, ticket_id: int) -> bool:
        """deletes a ticket"""

        query = (
            ticket_table
            .delete()
            .where(ticket_table.c.id == ticket_id)
        )
        result = await database.execute(query)

        return bool(result)

    async def get_by_user_id(self, user_id: UUID) -> Iterable[Any]:
        """retrieves a ticket by user_id"""

        query = (ticket_table.select().where(ticket_table.c.user_id == str(user_id)))
        tickets = await database.fetch_all(query)
        return tickets
