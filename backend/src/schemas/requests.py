from __future__ import annotations
from pydantic import BaseModel, ConfigDict, field_validator, model_validator
from datetime import datetime
from typing import Optional, Literal
from src.enums import RequestStatusEnum, FamilyMemberCountEnum, PetExperienceEnum, AdoptionPurposeEnum, HousingTypeEnum, HousingAreaEnum, RequestTypeEnum


class RequestBaseSchema(BaseModel):
    dog_id: int
    full_name: str
    phone: str
    email: str
    status: RequestStatusEnum


class RequestCreateSchema(RequestBaseSchema):
    type: RequestTypeEnum
    adoption_details: Optional[AdoptionRequestBaseSchema] = None
    guardian_details: Optional[GuardianRequestBaseSchema] = None

    @field_validator('adoption_details')
    @classmethod
    def validate_adoption_details(cls, v, info):
        req_type = info.data.get('type')
        if req_type == RequestTypeEnum.ADOPTION_REQUEST and v is None:
            raise ValueError("Для подачи заявки на усыновление необходимо предоставить подробную информацию об усыновлении")
        return v

    @field_validator('guardian_details')
    @classmethod
    def validate_guardian_details(cls, v, info):
        req_type = info.data.get('type')
        if req_type == RequestTypeEnum.GUARDIAN_REQUEST and v is None:
            return GuardianRequestBaseSchema()
        return v

    @model_validator(mode='after')
    def validate_mutually_exclusive_details(self) -> 'RequestCreateSchema':
        if self.adoption_details is not None and self.guardian_details is not None:
            raise ValueError(
                "Нельзя передавать одновременно guardian_details и adoption_details"
            )
        if self.adoption_details and self.type != RequestTypeEnum.ADOPTION_REQUEST:
            raise ValueError("Тип заявки должен быть Усыновление, если указано поле adoption_details")

        if self.guardian_details  and self.type != RequestTypeEnum.GUARDIAN_REQUEST:
            raise ValueError("Тип заявки должен быть Опека, если указано поле guardian_details")
        return self


class RequestResponseSchema(RequestBaseSchema):
    id: int
    created_at: datetime
    closed_at: Optional[datetime] = None
    type: RequestTypeEnum
    adoption_request: Optional[AdoptionRequestBaseSchema] = None
    guardian_request: Optional[GuardianRequestBaseSchema] = None

    model_config = ConfigDict(from_attributes=True)

class AdoptionRequestBaseSchema(BaseModel):
    family_member_count: FamilyMemberCountEnum
    had_experience_adoption_pet: PetExperienceEnum
    adoption_purpose: AdoptionPurposeEnum
    housing_type: HousingTypeEnum
    housing_area: HousingAreaEnum


class AdoptionRequestCreateSchema(AdoptionRequestBaseSchema):
    pass


class AdoptionRequestResponseSchema(AdoptionRequestBaseSchema):
    id: int
    request_id: int

    model_config = ConfigDict(from_attributes=True)


class GuardianRequestBaseSchema(BaseModel):
    pass


class GuardianRequestCreateSchema(GuardianRequestBaseSchema):
    pass


class GuardianRequestResponseSchema(GuardianRequestBaseSchema):
    id: int
    request_id: int

    model_config = ConfigDict(from_attributes=True)