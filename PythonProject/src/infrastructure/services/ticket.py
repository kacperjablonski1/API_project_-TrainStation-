"""A module containing ticket service implementation."""

from typing import Iterable
from uuid import UUID

from src.core.domain.payment import PaymentIn
from src.core.repositories.iWallet import IWalletRepository
from src.core.domain.ticket import TicketIn
from src.core.repositories.ipayment import IPaymentRepository
from src.core.repositories.iticket import ITicketRepository
from src.infrastructure.dto.ticketdto import TicketDTO
from src.infrastructure.services.ipayment import IPaymentService
from src.infrastructure.services.iticket import ITicketService
from fastapi import HTTPException


class TicketService(ITicketService):
    """A class implementing ticket service."""

    _repository: ITicketRepository

    def __init__(self, ticket_repository: ITicketRepository, wallet_repository: IWalletRepository, payment_repository: IPaymentRepository) -> None:
        """Initialize ticket service."""
        self._ticket_repository = ticket_repository
        self._wallet_repository = wallet_repository
        self._payment_repository = payment_repository

    async def add_ticket(self, ticket: TicketIn) -> TicketDTO | None:
        """Create new ticket"""
        wallet = await self._wallet_repository.get_by_user_id(ticket.user_id)
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")

        if wallet.balance < ticket.price:
            raise HTTPException(status_code=400, detail="Not enough funds")

        updated = await self._wallet_repository.update_balance(
            user_id=ticket.user_id,
            amount=-ticket.price
        )
        if not updated:
            raise HTTPException(status_code=500, detail="Failed to update wallet")

        ticket_data = await self._ticket_repository.add_ticket(ticket)
        if not ticket_data:
            raise HTTPException(status_code=500, detail="Failed to create ticket")

        payment = PaymentIn(
            user_id = ticket.user_id,
            ticket_id = ticket_data["id"],
            amount = ticket.price,
            method = "wallet",
            status = "zaplacono"
        )
        await self._payment_repository.create_payment(payment)

        return TicketDTO.model_validate(ticket_data)

    async def get_by_id(self, ticket_id: int) -> TicketDTO | None:
        """Get ticket by id"""
        ticket = await self._ticket_repository.get_by_id(ticket_id)
        return TicketDTO.model_validate(ticket) if ticket else None

    async def get_all(self) -> Iterable[TicketDTO]:
        """Get all tickets"""
        tickets = await self._ticket_repository.get_all()
        return [TicketDTO.model_validate(t) for t in tickets]

    async def delete_ticket(self, ticket_id: int) -> bool:
        """Delete ticket"""
        return await self._ticket_repository.delete_ticket(ticket_id)

    async def get_by_user_id(self, user_id: UUID) -> Iterable[TicketDTO]:
        """Get ticket by user_id"""
        tickets = await self._ticket_repository.get_by_user_id(user_id)
        return [TicketDTO.model_validate(t) for t in tickets]
