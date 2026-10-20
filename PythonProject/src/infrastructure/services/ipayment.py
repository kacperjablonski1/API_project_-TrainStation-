"""A module containing payment service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable
from uuid import UUID
from src.core.domain.payment import PaymentIn
from src.infrastructure.dto.paymentdto import PaymentDTO


class IPaymentService(ABC):
    """An abstract class for payment service."""

    @abstractmethod
    async def create_payment(self, payment: PaymentIn) -> PaymentDTO | None:
        """Register new payment."""

    @abstractmethod
    async def get_by_id(self, payment_id: int) -> PaymentDTO | None:
        """Get payment by id."""

    @abstractmethod
    async def get_all_by_user(self, user_id: UUID) -> Iterable[PaymentDTO]:
        """Get all payments for user."""

    @abstractmethod
    async def update_status(
        self,
        payment_id: int,
        status: str,
    ) -> PaymentDTO | None:
        """Update payment status."""

    @abstractmethod
    async def get_all_by_status(self, status: str) -> Iterable[PaymentDTO]:
        """Get payments by status."""
