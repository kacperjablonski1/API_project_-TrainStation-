from abc import ABC, abstractmethod
from typing import Any
from src.core.domain.payment import WalletIn
from uuid import UUID
class IWalletRepository(ABC):


    @abstractmethod
    async def create_wallet(self, wallet: WalletIn) -> Any | None:
        """
        create new wallet
        """

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> Any | None:
        """
        get wallet by user id
        """

    @abstractmethod
    async def update_balance(self, user_id: UUID, amount: float) -> bool:
        """
        update wallet balance
        """
