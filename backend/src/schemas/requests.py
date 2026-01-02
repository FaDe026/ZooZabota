from pydantic import BaseModel, ConfigDict
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


class RequestResponseSchema(RequestBaseSchema):
    id: int
    created_at: datetime
    closed_at: Optional[datetime] = None
    type: RequestTypeEnum

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