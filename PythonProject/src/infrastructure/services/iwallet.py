"""A module containing wallet service abstractions."""

from abc import ABC, abstractmethod
from src.core.domain.payment import WalletIn
from src.infrastructure.dto.paymentdto import WalletDTO
from uuid import UUID

class IWalletService(ABC):
    """An abstract class for wallet service."""

    @abstractmethod
    async def create_wallet(self, wallet: WalletIn) -> WalletDTO | None:
        """Create a new wallet for a user."""

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> WalletDTO | None:
        """Get wallet by user id."""

    @abstractmethod
    async def update_balance(self, user_id: UUID, amount: float) -> bool:
        """Update wallet balance by amount."""
