from pydantic import BaseModel, ConfigDict, UUID4



class TrainStationIn(BaseModel):
    name: str
    city: str

class TrainStationBroker(TrainStationIn):
    user_id: UUID4

class TrainStation(TrainStationBroker):
    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")
