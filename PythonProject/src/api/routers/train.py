"""A module containing train endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from src.container import Container
from src.core.domain.train import TrainIn
from src.infrastructure.dto.traindto import TrainDTO
from src.infrastructure.services.itrain import ITrainService

router = APIRouter()


@router.post("/create", response_model=TrainDTO, status_code=201)
@inject
async def create_train(
    train: TrainIn,
    service: ITrainService = Depends(Provide[Container.train_service]),
) -> dict:
    """Endpoint for adding a new train."""
    if new_train := await service.add_train(train):
        return TrainDTO.model_validate(new_train).model_dump()

    raise HTTPException(
        status_code=400,
        detail="Failed to create train"
    )


@router.get("/all", response_model=Iterable[TrainDTO], status_code=200)
@inject
async def get_all_trains(
    service: ITrainService = Depends(Provide[Container.train_service]),
) -> Iterable:
    """Endpoint for getting all trains."""
    trains = await service.get_all()
    return [TrainDTO.model_validate(t).model_dump() for t in trains]


@router.get("/id", response_model=TrainDTO, status_code=200)
@inject
async def get_train_by_id(
    train_id: int,
    service: ITrainService = Depends(Provide[Container.train_service]),
) -> dict:
    """Endpoint for getting a train by ID."""
    if train := await service.get_by_id(train_id):
        return TrainDTO.model_validate(train).model_dump()

    raise HTTPException(
        status_code=404,
        detail="Train not found"
    )


@router.delete("/delete", status_code=204)
@inject
async def delete_train(
    train_id: int,
    service: ITrainService = Depends(Provide[Container.train_service]),
) -> None:
    """Endpoint for deleting a train by ID."""
    if await service.delete_train(train_id):
        return

    raise HTTPException(
        status_code=404,
        detail="Train not found"
    )
