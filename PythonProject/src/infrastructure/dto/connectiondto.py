"""A module containing DTO model for connection."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ConnectionDTO(BaseModel):
    """A DTO model for train connection."""

    id: int
    train_id: int
    departure_station_id: int
    arrival_station_id: int
    departure_time: datetime
    arrival_time: datetime
    duration_minutes: int

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )
