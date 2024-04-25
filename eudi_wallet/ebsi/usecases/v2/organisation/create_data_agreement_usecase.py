from logging import Logger
from typing import List, Optional

from jsonschema import exceptions, validate

from eudi_wallet.ebsi.exceptions.application.organisation import (
    CreateDataAgreementUsecaseError,
)
from eudi_wallet.ebsi.models.v2.data_agreement import V2DataAgreementModel
from eudi_wallet.ebsi.repositories.v2.data_agreement import (
    SqlAlchemyV2DataAgreementRepository,
)
from eudi_wallet.ebsi.utils.jsonschema import meta_schema_draft_7
from eudi_wallet.ebsi.utils.common import convert_data_attributes_to_json_schema


class CreateV2DataAgreementUsecase:
    def __init__(
        self,
        dataagreement_repository: SqlAlchemyV2DataAgreementRepository,
        logger: Logger,
    ) -> None:
        self.dataagreement_repository = dataagreement_repository
        self.logger = logger

    def _convert_sentence_to_pascal_case(self, sentence: str) -> str:
        words = sentence.split()
        if len(words) > 1:
            return "".join(word.strip().capitalize() for word in words)
        else:
            return sentence

    def execute(
        self,
        organisation_id: str,
        purpose: str,
        data_attributes: list,
        exchange_mode: str,
        purpose_description: str,
        limited_disclosure: bool,
        credential_types: Optional[List[str]] = None,
    ) -> V2DataAgreementModel:
        if not credential_types:
            credential_types = [
                "VerifiableCredential",
                self._convert_sentence_to_pascal_case(purpose),
            ]

        try:
            data_attributes_json_schema = convert_data_attributes_to_json_schema(data_attributes=data_attributes)
            validate(instance=data_attributes_json_schema, schema=meta_schema_draft_7)
        except exceptions.ValidationError as e:
            raise CreateDataAgreementUsecaseError(e.message)
        with self.dataagreement_repository as repo:
            existing_agreement = repo.get_by_purpose_and_organisation_id(organisation_id, purpose)
            if existing_agreement:
                error_message = f"A data agreement with purpose '{purpose}' already exists."
                self.logger.error(error_message)
                raise CreateDataAgreementUsecaseError(error_message)
            
            return repo.create(
                organisation_id=organisation_id,
                purpose=purpose,
                data_attributes=data_attributes,
                exchange_mode=exchange_mode,
                credential_types=credential_types,
                purpose_description=purpose_description,
                limited_disclosure=limited_disclosure,
            )
