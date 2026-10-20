"""A module containing ticket service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from src.core.domain.ticket import Ticket, TicketIn
from src.infrastructure.dto.ticketdto import TicketDTO
from uuid import UUID

class ITicketService(ABC):
    """An abstract class for ticket service."""

    @abstractmethod
    async def add_ticket(self, ticket: TicketIn) -> TicketDTO | None:
        """Add new ticket."""

    @abstractmethod
    async def get_by_id(self, ticket_id: int) -> TicketDTO | None:
        """Get ticket by id."""

    @abstractmethod
    async def get_all(self) -> Iterable[TicketDTO]:
        """Get all tickets."""

    @abstractmethod
    async def delete_ticket(self, ticket_id: int) -> bool:
        """Delete ticket."""

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> Iterable[TicketDTO]:
        """Get all tickets belonging to a specific user."""