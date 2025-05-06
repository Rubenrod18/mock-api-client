"""Module for managing dependency injections."""

from dependency_injector import containers, providers

from app import services


class ServiceDIContainer(containers.DeclarativeContainer):
    """Service Dependency Injection Container."""

    config = providers.Configuration()
    wiring_config = containers.WiringConfiguration(
        modules=[
            '.blueprints.posts',
        ]
    )

    # Services
    post_service = providers.Factory(services.PostService)
