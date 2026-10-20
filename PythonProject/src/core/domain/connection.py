from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ConnectionIn(BaseModel):

    train_id: int
    departure_station_id: int
    arrival_station_id: int
    departure_time: datetime
    arrival_time: datetime
    duration_minutes: int

class Connection(ConnectionIn):
    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")
