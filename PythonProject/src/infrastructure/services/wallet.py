"""A module containing wallet service implementation."""

from src.core.domain.payment import WalletIn
from src.core.repositories.iWallet import IWalletRepository
from src.infrastructure.dto.paymentdto import WalletDTO
from src.infrastructure.services.iwallet import IWalletService
from uuid import UUID

class WalletService(IWalletService):
    """A class implementing wallet service."""

    _repository: IWalletRepository

    def __init__(self, repository: IWalletRepository) -> None:
        """Initialize wallet service."""
        self._repository = repository

    async def create_wallet(self, wallet: WalletIn) -> WalletDTO | None:
        """Create new wallet."""
        if new_wallet := await self._repository.create_wallet(wallet):
            return WalletDTO.model_validate(new_wallet)
        return None

    async def get_by_user_id(self, user_id: UUID) -> WalletDTO | None:
        """Get wallet by user id."""
        if wallet := await self._repository.get_by_user_id(user_id):
            return WalletDTO.model_validate(wallet)
        return None

    async def update_balance(self, user_id: UUID, amount: float) -> bool:
        """Update wallet balance."""
        return await self._repository.update_balance(user_id, amount)
