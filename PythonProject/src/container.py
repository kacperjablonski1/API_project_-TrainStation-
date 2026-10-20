"""Module providing containers injecting dependencies for your project."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from src.infrastructure.repositories.user import UserRepository
from src.infrastructure.repositories.ticket import TicketRepository
from src.infrastructure.repositories.payment import PaymentRepository
from src.infrastructure.repositories.wallet import WalletRepository
from src.infrastructure.repositories.train import TrainRepository
from src.infrastructure.repositories.trainStation import TrainStationRepository
from src.infrastructure.repositories.connection import ConnectionRepository

from src.infrastructure.services.ticket import TicketService
from src.infrastructure.services.payment import PaymentService
from src.infrastructure.services.wallet import WalletService
from src.infrastructure.services.train import TrainService
from src.infrastructure.services.trainStation import TrainStationService
from src.infrastructure.services.connection import ConnectionService
from src.infrastructure.services.user import UserService


class Container(DeclarativeContainer):
    """Container class for dependency injection."""

    user_repository = Singleton(UserRepository)
    ticket_repository = Singleton(TicketRepository)
    payment_repository = Singleton(PaymentRepository)
    wallet_repository = Singleton(WalletRepository)
    train_repository = Singleton(TrainRepository)
    train_station_repository = Singleton(TrainStationRepository)
    connection_repository = Singleton(ConnectionRepository)

    ticket_service = Factory(
        TicketService,
        ticket_repository=ticket_repository,
        wallet_repository=wallet_repository,
        payment_repository=payment_repository,
    )

    payment_service = Factory(
        PaymentService,
        repository=payment_repository,
        ticket_repository=ticket_repository,
    )

    wallet_service = Factory(
        WalletService,
        repository=wallet_repository,
    )

    train_service = Factory(
        TrainService,
        repository=train_repository,
    )

    train_station_service = Factory(
        TrainStationService,
        repository=train_station_repository,
    )

    connection_service = Factory(
        ConnectionService,
        repository=connection_repository,
        station_repository=train_station_repository,
    )

    user_service = Factory(
        UserService,
        repository=user_repository,
    )
