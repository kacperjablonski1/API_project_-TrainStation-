from abc import ABC, abstractmethod
from typing import Any, Iterable
from src.core.domain.ticket import TicketIn
from uuid import UUID

class ITicketRepository(ABC):

    @abstractmethod
    async def add_ticket(self, ticket: TicketIn) -> Any | None:
        """
        create new ticket
        """

    @abstractmethod
    async def get_by_id(self, ticket_id: int) -> Any | None:
        """
        get ticket by id
        """

    @abstractmethod
    async def get_all(self) -> Iterable[Any]:
        """
        returns a list of tickets
        """

    @abstractmethod
    async def delete_ticket(self, ticket_id: int) -> bool:
        """
        delete ticket
        """
    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> Iterable[Any]:

        """
        get ticket by user_id
        """
