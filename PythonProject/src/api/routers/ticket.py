"""A module containing ticket-related endpoints."""

from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from src.container import Container
from src.core.domain.ticket import TicketIn
from src.infrastructure.dto.ticketdto import TicketDTO
from src.infrastructure.services.iticket import ITicketService

router = APIRouter()


@router.post("/create", response_model=TicketDTO, status_code=201)
@inject
async def create_ticket(
    ticket: TicketIn,
    service: ITicketService = Depends(Provide[Container.ticket_service]),
) -> dict:
    """Endpoint for creating a new ticket.

    Args:
        ticket (TicketIn): Ticket input data.
        service (ITicketService, optional): Injected ticket service.

    Returns:
        dict: Created ticket details.
    """
    new_ticket = await service.add_ticket(ticket)
    if new_ticket:
        return new_ticket.model_dump()

    raise HTTPException(
        status_code=400,
        detail="Failed to create ticket"
    )


@router.get("/id", response_model=TicketDTO, status_code=200)
@inject
async def get_ticket_by_id(
    ticket_id: int,
    service: ITicketService = Depends(Provide[Container.ticket_service]),
) -> dict:
    """Endpoint for getting ticket by ID.

    Args:
        ticket_id (int): Ticket ID.
        service (ITicketService, optional): Injected ticket service.

    Returns:
        dict: Ticket details.
    """
    if ticket := await service.get_by_id(ticket_id):
        return ticket.model_dump()

    raise HTTPException(
        status_code=404,
        detail="Ticket not found"
    )


@router.get("/all", response_model=Iterable[TicketDTO], status_code=200)
@inject
async def get_all_tickets(
    service: ITicketService = Depends(Provide[Container.ticket_service]),
) -> Iterable[TicketDTO]:
    """Endpoint for getting all tickets.

    Args:
        service (ITicketService, optional): Injected ticket service.

    Returns:
        Iterable[TicketDTO]: List of all tickets.
    """
    tickets = await service.get_all()
    return tickets


@router.delete("/delete", status_code=204, include_in_schema=False)
@inject
async def delete_ticket(
    ticket_id: int,
    service: ITicketService = Depends(Provide[Container.ticket_service]),
) -> None:
    """Endpoint for deleting a ticket by ID.

    Args:
        ticket_id (int): Ticket ID.
        service (ITicketService, optional): Injected ticket service.

    Raises:
        HTTPException: If ticket does not exist.
    """
    if await service.delete_ticket(ticket_id):
        return

    raise HTTPException(
        status_code=404,
        detail="Ticket not found"
    )


@router.get("/user", response_model=Iterable[TicketDTO], status_code=200)
@inject
async def get_ticket_by_user(
    user_id: UUID,
    service: ITicketService = Depends(Provide[Container.ticket_service]),
)-> Iterable[TicketDTO]:
    """Endpoint for getting ticket by user.
    Args:
    """
    return await service.get_by_user_id(user_id)