"""A module containing connection-related endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from src.container import Container
from src.core.domain.connection import ConnectionIn
from src.infrastructure.dto.connectiondto import ConnectionDTO
from src.infrastructure.services.iconnection import IConnectionService

router = APIRouter()

@router.post("/create", response_model=ConnectionDTO, status_code=201)
@inject
async def create_connection(
    connection: ConnectionIn,
    service: IConnectionService = Depends(Provide[Container.connection_service]),
) -> dict:
    """Endpoint for creating a new train connection.

    Args:
        connection (ConnectionIn): Input data for the new connection.
        service (IConnectionService, optional): Injected connection service.

    Returns:
        dict: Created connection details.
    """
    new_connection = await service.create_connection(connection)
    if new_connection:
        return new_connection.model_dump()

    raise HTTPException(status_code=400, detail="Failed to create connection")


@router.get("/search", response_model=Iterable[ConnectionDTO], status_code=200)
@inject
async def search_connections(
    start_city: str,
    end_city: str,
    service: IConnectionService = Depends(Provide[Container.connection_service]),
) -> Iterable[ConnectionDTO]:
    """Endpoint for searching connections between two stations.

    Args:

        service (IConnectionService, optional): Injected connection service.

    Returns:
        Iterable[ConnectionDTO]: List of connections matching the search.
    """
    return await service.search_by_city(start_city, end_city)


@router.get("/id", response_model=ConnectionDTO, status_code=200)
@inject
async def get_connection_by_id(
    connection_id: int,
    service: IConnectionService = Depends(Provide[Container.connection_service]),
) -> dict:
    """Endpoint for retrieving a connection by its ID.

    Args:
        connection_id (int): Connection ID.
        service (IConnectionService, optional): Injected connection service.

    Returns:
        dict: Connection details.
    """
    if connection := await service.get_by_id(connection_id):
        return connection.model_dump()

    raise HTTPException(status_code=404, detail="Connection not found")


@router.get("/all", response_model=Iterable[ConnectionDTO], status_code=200)
@inject
async def get_all_connections(
    service: IConnectionService = Depends(Provide[Container.connection_service]),
) -> Iterable[ConnectionDTO]:
    """Endpoint for retrieving all connections.

    Args:
        service (IConnectionService, optional): Injected connection service.

    Returns:
        Iterable[ConnectionDTO]: List of all connections.
    """
    return await service.get_all_connections()


