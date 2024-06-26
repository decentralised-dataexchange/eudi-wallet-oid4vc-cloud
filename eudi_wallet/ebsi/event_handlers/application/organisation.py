from logging import Logger

from sqlalchemy.orm import Session

from eudi_wallet.ebsi.events.application.organisation import (
    OnboardTrustedAccreditationOrganisationEvent,
    OnboardTrustedIssuerEvent,
)
from eudi_wallet.ebsi.repositories.credential_revocation_status_list import (
    SqlAlchemyCredentialRevocationStatusListRepository,
)
from eudi_wallet.ebsi.repositories.organisation import SqlAlchemyOrganisationRepository
from eudi_wallet.ebsi.services.application.organisation import OrganisationService
from eudi_wallet.ebsi.value_objects.domain.discovery import (
    OpenIDAuthServerConfig,
    OpenIDCredentialIssuerConfig,
)


async def handle_event_onboard_trusted_issuer(
    event: OnboardTrustedIssuerEvent, logger: Logger, db_session: Session
):
    credential_issuer_configuration = OpenIDCredentialIssuerConfig.from_dict(
        event.openid_credential_issuer_config
    )
    auth_server_configuration = OpenIDAuthServerConfig.from_dict(
        event.auth_server_config
    )

    legal_entity_repository = SqlAlchemyOrganisationRepository(
        session=db_session, logger=logger
    )
    credential_revocation_status_list_repository = (
        SqlAlchemyCredentialRevocationStatusListRepository(
            session=db_session, logger=logger
        )
    )
    legal_entity_service = OrganisationService(
        credential_issuer_configuration=credential_issuer_configuration,
        auth_server_configuration=auth_server_configuration,
        logger=logger,
        issuer_domain=event.issuer_domain,
        legal_entity_repository=legal_entity_repository,
        credential_revocation_status_list_repository=credential_revocation_status_list_repository,
    )
    legal_entity_entity = await legal_entity_service.get_first_legal_entity()
    if legal_entity_entity:
        await legal_entity_service.set_cryptographic_seed(
            crypto_seed=legal_entity_entity.cryptographic_seed
        )
        await legal_entity_service.set_entity(legal_entity_entity=legal_entity_entity)
        await legal_entity_service.onboard_trusted_issuer()


async def handle_event_onboard_trusted_accreditation_organisation(
    event: OnboardTrustedAccreditationOrganisationEvent,
    logger: Logger,
    db_session: Session,
):
    credential_issuer_configuration = OpenIDCredentialIssuerConfig.from_dict(
        event.openid_credential_issuer_config
    )
    auth_server_configuration = OpenIDAuthServerConfig.from_dict(
        event.auth_server_config
    )

    legal_entity_repository = SqlAlchemyOrganisationRepository(
        session=db_session, logger=logger
    )
    credential_revocation_status_list_repository = (
        SqlAlchemyCredentialRevocationStatusListRepository(
            session=db_session, logger=logger
        )
    )
    legal_entity_service = OrganisationService(
        credential_issuer_configuration=credential_issuer_configuration,
        auth_server_configuration=auth_server_configuration,
        logger=logger,
        issuer_domain=event.issuer_domain,
        legal_entity_repository=legal_entity_repository,
        credential_revocation_status_list_repository=credential_revocation_status_list_repository,
    )
    legal_entity_entity = await legal_entity_service.get_first_legal_entity()
    if legal_entity_entity:
        await legal_entity_service.set_cryptographic_seed(
            crypto_seed=legal_entity_entity.cryptographic_seed
        )
        await legal_entity_service.set_entity(legal_entity_entity=legal_entity_entity)
        await legal_entity_service.onboard_trusted_accreditation_organisation()


async def handle_event_onboard_root_trusted_accreditation_organisation(
    event: OnboardTrustedAccreditationOrganisationEvent,
    logger: Logger,
    db_session: Session,
):
    credential_issuer_configuration = OpenIDCredentialIssuerConfig.from_dict(
        event.openid_credential_issuer_config
    )
    auth_server_configuration = OpenIDAuthServerConfig.from_dict(
        event.auth_server_config
    )

    legal_entity_repository = SqlAlchemyOrganisationRepository(
        session=db_session, logger=logger
    )
    credential_revocation_status_list_repository = (
        SqlAlchemyCredentialRevocationStatusListRepository(
            session=db_session, logger=logger
        )
    )
    legal_entity_service = OrganisationService(
        credential_issuer_configuration=credential_issuer_configuration,
        auth_server_configuration=auth_server_configuration,
        logger=logger,
        issuer_domain=event.issuer_domain,
        legal_entity_repository=legal_entity_repository,
        credential_revocation_status_list_repository=credential_revocation_status_list_repository,
    )
    legal_entity_entity = await legal_entity_service.get_first_legal_entity()
    if legal_entity_entity:
        await legal_entity_service.set_cryptographic_seed(
            crypto_seed=legal_entity_entity.cryptographic_seed
        )
        await legal_entity_service.set_entity(legal_entity_entity=legal_entity_entity)
        await legal_entity_service.onboard_root_trusted_accreditation_organisation()
