from typing import Any, Iterable

from src.core.domain.payment import PaymentIn
from src.core.repositories.ipayment import IPaymentRepository
from src.db import database, payment_table
from uuid import UUID

class PaymentRepository(IPaymentRepository):

    async def create_payment(self, payment: PaymentIn) -> Any | None:
        """registers a new payment"""

        query = payment_table.insert().values(**payment.model_dump())
        new_payment_id = await database.execute(query)

        return await self.get_by_id(new_payment_id)

    async def get_by_id(self, payment_id: int) -> Any | None:
        """gets payment by id"""

        query = (
            payment_table
            .select()
            .where(payment_table.c.id == payment_id)
        )
        payment = await database.fetch_one(query)

        return payment

    async def get_all_by_user(self, user_id: UUID) -> Iterable[Any]:
        """Returns all payments"""

        query = (
            payment_table
            .select()
            .where(payment_table.c.user_id == user_id)
        )
        payments = await database.fetch_all(query)

        return payments

    async def update_status(self, payment_id: int, status: str) -> Any | None:
        """Updates payment status"""

        query = (
            payment_table
            .update()
            .where(payment_table.c.id == payment_id)
            .values(status=status)
        )
        await database.execute(query)

        return await self.get_by_id(payment_id)

    async def get_all_by_status(self, status: str) -> Iterable[Any]:
        """Returns all payments by status"""

        query = (
            payment_table
            .select()
            .where(payment_table.c.status == status)
        )
        payments = await database.fetch_all(query)

        return payments
