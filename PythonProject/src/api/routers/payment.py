"""A module containing payment-related endpoints."""

from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from src.container import Container
from src.core.domain.payment import PaymentIn
from src.infrastructure.dto.paymentdto import PaymentDTO
from src.infrastructure.services.ipayment import IPaymentService

router = APIRouter()


@router.post("/create", response_model=PaymentDTO, status_code=201, include_in_schema=False)
@inject
async def create_payment(
    payment: PaymentIn,
    service: IPaymentService = Depends(Provide[Container.payment_service]),
) -> dict:
    """Endpoint for creating a new payment.

    Args:
        payment (PaymentIn): Payment input data.
        service (IPaymentService, optional): Injected payment service.

    Returns:
        dict: Created payment details.
    """
    new_payment = await service.create_payment(payment)
    if new_payment:
        return new_payment.model_dump()

    raise HTTPException(
        status_code=400,
        detail="Failed to create payment"
    )


@router.get("/id", response_model=PaymentDTO, status_code=200)
@inject
async def get_payment_by_id(
    payment_id: int,
    service: IPaymentService = Depends(Provide[Container.payment_service]),
) -> dict:
    """Endpoint for getting payment by ID.

    Args:
        payment_id (int): Payment ID.
        service (IPaymentService, optional): Injected payment service.

    Returns:
        dict: Payment details.
    """
    if payment := await service.get_by_id(payment_id):
        return payment.model_dump()

    raise HTTPException(
        status_code=404,
        detail="Payment not found"
    )


@router.get("/user", response_model=Iterable[PaymentDTO], status_code=200)
@inject
async def get_payments_by_user(
    user_id: UUID,
    service: IPaymentService = Depends(Provide[Container.payment_service]),
) -> Iterable[PaymentDTO]:
    """Endpoint for getting all payments for a user.

    Args:
        user_id (int): User ID.
        service (IPaymentService, optional): Injected payment service.

    Returns:
        Iterable[PaymentDTO]: List of payments for the user.
    """
    payments = await service.get_all_by_user(user_id)
    return payments


@router.put("/update", response_model=PaymentDTO, status_code=200, include_in_schema=False)
@inject
async def update_payment_status(
    payment_id: int,
    status: str,
    service: IPaymentService = Depends(Provide[Container.payment_service]),
) -> dict:
    """Endpoint for updating payment status.

    Args:
        payment_id (int): Payment ID.
        status (str): New status of the payment.
        service (IPaymentService, optional): Injected payment service.

    Returns:
        dict: Updated payment details.
    """
    updated_payment = await service.update_status(payment_id, status)
    if updated_payment:
        return updated_payment.model_dump()

    raise HTTPException(
        status_code=404,
        detail="Payment not found or status not updated"
    )


@router.get("/status", response_model=Iterable[PaymentDTO], status_code=200, include_in_schema=False)
@inject
async def get_payments_by_status(
    status: str,
    service: IPaymentService = Depends(Provide[Container.payment_service]),
) -> Iterable[PaymentDTO]:
    """Endpoint for getting all payments by status.

    Args:
        status (str): Payment status to filter by.
        service (IPaymentService, optional): Injected payment service.

    Returns:
        Iterable[PaymentDTO]: List of payments with the given status.
    """
    payments = await service.get_all_by_status(status)
    return payments
