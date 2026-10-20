from typing import Optional
from pydantic import BaseModel, ConfigDict

class TrainIn(BaseModel):
    number: str
    name: Optional[str] = None

class Train(TrainIn):
    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")
