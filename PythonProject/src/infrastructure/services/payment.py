"""A module containing payment service implementation."""

from typing import Iterable

from fastapi import HTTPException

from src.core.domain.payment import PaymentIn
from src.core.repositories.ipayment import IPaymentRepository
from src.core.repositories.iticket import ITicketRepository
from src.infrastructure.dto.paymentdto import PaymentDTO
from src.infrastructure.services.ipayment import IPaymentService
from uuid import UUID


class PaymentService(IPaymentService):
    """A class implementing payment service."""

    _repository: IPaymentRepository

    def __init__(self, repository: IPaymentRepository, ticket_repository: ITicketRepository) -> None:
        """Initialize the payment service."""
        self._repository = repository
        self._ticket_repository = ticket_repository

    async def create_payment(self, payment: PaymentIn) -> PaymentDTO | None:
        """Create new payment."""
        ticket = await self._ticket_repository.get_by_id(payment.ticket_id)
        if not ticket:
            raise HTTPException(
                status_code = 400,
                detail = f"Wrong ticket id"
            )

        db_payment = await self._repository.create_payment(payment)
        if db_payment:
            return PaymentDTO(**db_payment)
        return None

    async def get_by_id(self, payment_id: int) -> PaymentDTO | None:
        """Get payment by id."""
        db_payment = await self._repository.get_by_id(payment_id)
        if db_payment:
            return PaymentDTO(**db_payment)
        return None

    async def get_all_by_user(self, user_id: UUID) -> Iterable[PaymentDTO]:
        """Get all payments for user."""
        payments = await self._repository.get_all_by_user(user_id)
        return [PaymentDTO(**p) for p in payments]

    async def update_status(self,payment_id: int,status: str) -> PaymentDTO | None:
        """Update payment status."""
        db_payment = await self._repository.update_status(payment_id, status)
        if db_payment:
            return PaymentDTO(**db_payment)
        return None

    async def get_all_by_status(self, status: str) -> Iterable[PaymentDTO]:
        """Get payments for status."""
        payments = await self._repository.get_all_by_status(status)
        return [PaymentDTO(**p) for p in payments]
