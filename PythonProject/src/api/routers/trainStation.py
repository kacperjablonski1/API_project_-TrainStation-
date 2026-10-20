"""A module containing train station endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt


from src.infrastructure.utils import consts
from src.container import Container
from src.core.domain.trainStation import TrainStation, TrainStationIn, TrainStationBroker
from src.infrastructure.dto.trainStationdto import TrainStationDTO
from src.infrastructure.services.itrainStation import ITrainStationService

bearer_scheme = HTTPBearer()
router = APIRouter()


@router.post("/create", response_model=TrainStationDTO, status_code=201)
@inject
async def create_station(
    station: TrainStationIn,
    service: ITrainStationService = Depends(Provide[Container.train_station_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")
    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    extended_station = TrainStationBroker(
        user_id=user_uuid,
        **station.model_dump()
    )

    new_station = await service.add_station(extended_station)

    return new_station.model_dump() if new_station else {}


@router.get("/all", response_model=Iterable[TrainStationDTO], status_code=200)
@inject
async def get_all_stations(
    service: ITrainStationService = Depends(Provide[Container.train_station_service]),
) -> Iterable:
    """Endpoint for getting all train stations."""
    stations = await service.get_all()
    return [TrainStationDTO.model_validate(s).model_dump() for s in stations]


@router.get("/id", response_model=TrainStationDTO, status_code=200)
@inject
async def get_station_by_id(
    station_id: int,
    service: ITrainStationService = Depends(Provide[Container.train_station_service]),
) -> dict:
    """Endpoint for getting a train station by ID."""
    if station := await service.get_by_id(station_id):
        return TrainStationDTO.model_validate(station).model_dump()

    raise HTTPException(status_code=404,detail="Station not found")


@router.delete("/delete", status_code=204)
@inject
async def delete_station(
    station_id: int,
    service: ITrainStationService = Depends(Provide[Container.train_station_service]),
) -> None:
    """Endpoint for deleting a train station by ID."""
    if await service.delete_station(station_id):
        return

    raise HTTPException(status_code=404,detail="Station not found" )
