"""A module containing DTO model for train."""

from typing import Optional
from pydantic import BaseModel, ConfigDict


class TrainDTO(BaseModel):
    """A DTO model for train."""

    id: int
    number: str
    name: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )
