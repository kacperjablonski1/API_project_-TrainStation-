from pydantic import BaseModel, ConfigDict
from uuid import UUID

class TicketIn(BaseModel):
    user_id: UUID
    connection_id: int
    seat_type: str
    ticket_type: str
    price: float
    passenger_name: str
    with_animal: bool = False
    with_disabled: bool = False


class Ticket(TicketIn):
    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")
