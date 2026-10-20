"""A module containing DTO model for ticket."""

from pydantic import BaseModel, ConfigDict
from uuid import UUID

class TicketDTO(BaseModel):
    """A DTO model for ticket."""
    id: int
    user_id: UUID
    connection_id: int
    seat_type: str
    ticket_type: str
    price: float
    passenger_name: str
    with_animal: bool
    with_disabled: bool

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )
