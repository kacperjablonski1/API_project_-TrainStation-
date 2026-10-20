"""A module containing DTO models for payment and wallet."""

from pydantic import BaseModel, ConfigDict
from uuid import UUID

class WalletDTO(BaseModel):
    """A DTO model for wallet."""
    id: int
    user_id: UUID
    balance: float

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )


class PaymentDTO(BaseModel):
    """A DTO model for payment."""
    id: int
    user_id: UUID
    ticket_id: int
    amount: float
    method: str
    status: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )
