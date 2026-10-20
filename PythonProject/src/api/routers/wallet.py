"""A module containing wallet endpoints."""

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from src.container import Container
from src.core.domain.payment import WalletIn
from src.infrastructure.dto.paymentdto import WalletDTO
from src.infrastructure.services.iwallet import IWalletService

router = APIRouter()


@router.post("/create", response_model=WalletDTO, status_code=201)
@inject
async def create_wallet(
    wallet: WalletIn,
    service: IWalletService = Depends(Provide[Container.wallet_service]),
) -> dict:
    """Endpoint for creating a wallet."""
    if new_wallet := await service.create_wallet(wallet):
        return WalletDTO.model_validate(new_wallet).model_dump()

    raise HTTPException(
        status_code=400,
        detail="Wallet for this user already exists"
    )


@router.get("/id", response_model=WalletDTO, status_code=200)
@inject
async def get_wallet_by_user(
    user_id: UUID,
    service: IWalletService = Depends(Provide[Container.wallet_service]),
) -> dict:
    """Endpoint to get wallet by user ID."""
    if wallet := await service.get_by_user_id(user_id):
        return WalletDTO.model_validate(wallet).model_dump()

    raise HTTPException(
        status_code=404,
        detail="Wallet not found"
    )


@router.put("/update", response_model=WalletDTO, status_code=200)
@inject
async def update_wallet_balance(
    user_id: UUID,
    amount: float,
    service: IWalletService = Depends(Provide[Container.wallet_service]),
) -> dict:
    """Endpoint to update wallet balance."""
    success = await service.update_balance(user_id, amount)
    if success:
        if updated_wallet := await service.get_by_user_id(user_id):
            return WalletDTO.model_validate(updated_wallet).model_dump()

    raise HTTPException(
        status_code=400,
        detail="Failed to update wallet balance"
    )
