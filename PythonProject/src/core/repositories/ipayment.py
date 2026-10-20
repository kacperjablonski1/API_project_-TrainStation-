from abc import ABC, abstractmethod
from typing import Any, Iterable
from src.core.domain.payment import PaymentIn
from uuid import UUID

class IPaymentRepository(ABC):

    @abstractmethod
    async def create_payment(self, payment: PaymentIn) -> Any | None:
        """
        Create a new payment
        """

    @abstractmethod
    async def get_by_id(self, payment_id: int) -> Any | None:
        """
        get payment by id
        """

    @abstractmethod
    async def get_all_by_user(self, user_id: UUID) -> Iterable[Any]:
        """
        returns all payments
        """

    @abstractmethod
    async def update_status(self, payment_id: int, status: str) -> Any | None:
        """
        Update status of payment
        """

    @abstractmethod
    async def get_all_by_status(self, status: str) -> Iterable[Any]:
        """
        returns all payments by status
        """
