"""A module containing DTO model for train station."""

from pydantic import BaseModel, ConfigDict


class TrainStationDTO(BaseModel):
    """A DTO model for train station."""

    id: int
    name: str
    city: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )
