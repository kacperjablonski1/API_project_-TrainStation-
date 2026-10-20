"""A repository for wallet entity."""

from typing import Any

from src.core.domain.payment import WalletIn
from src.core.repositories.iWallet import IWalletRepository
from src.db import database, wallet_table
from uuid import UUID

class WalletRepository(IWalletRepository):

    async def create_wallet(self, wallet: WalletIn) -> Any | None:
        """create a new wallet"""

        existing = await self.get_by_user_id(wallet.user_id)
        if existing:
            return None

        query = wallet_table.insert().values(**wallet.model_dump())
        wallet_id = await database.execute(query)

        return await self.get_by_user_id(wallet.user_id)

    async def get_by_user_id(self, user_id: UUID) -> Any | None:
        """Retrieves a wallet by user_id"""

        query = (
            wallet_table
            .select()
            .where(wallet_table.c.user_id == user_id)
        )
        wallet = await database.fetch_one(query)

        return wallet

    async def update_balance(self, user_id: UUID, amount: float) -> bool:
        """Update the wallet balance """

        wallet = await self.get_by_user_id(user_id)
        if not wallet:
            return False

        new_balance = wallet["balance"] + amount

        query = (
            wallet_table
            .update()
            .where(wallet_table.c.user_id == user_id)
            .values(balance=new_balance)
        )

        await database.execute(query)
        return True
