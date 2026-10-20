from pydantic import BaseModel, ConfigDict
from uuid import UUID


class WalletIn(BaseModel):
    user_id: UUID
    balance: float = 0.0

class Wallet(WalletIn):
    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")

class PaymentIn(BaseModel):
    user_id: UUID
    ticket_id: int
    amount: float
    method: str
    status: str

class Payment(PaymentIn):
    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")
