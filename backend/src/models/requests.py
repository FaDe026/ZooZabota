from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from datetime import datetime
from typing import Optional
from src.enums import RequestStatusEnum, FamilyMemberCountEnum, PetExperienceEnum, AdoptionPurposeEnum, HousingTypeEnum, HousingAreaEnum, RequestTypeEnum

class RequestModel(Base):
    __tablename__ = 'request'

    id: Mapped[int] = mapped_column(primary_key=True)
    dog_id: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.today)
    closed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    type: Mapped[RequestTypeEnum] = mapped_column(nullable=False)
    full_name: Mapped[str]
    phone: Mapped[str]
    email: Mapped[str]
    status: Mapped[RequestStatusEnum]



class AdoptionRequestModel(Base):
    __tablename__ = 'adoption_request'

    id: Mapped[int] = mapped_column(primary_key=True)
    request_id: Mapped[int] = mapped_column(nullable=False, unique=True)

    family_member_count: Mapped[FamilyMemberCountEnum]
    had_experience_adoption_pet: Mapped[PetExperienceEnum]
    adoption_purpose: Mapped[AdoptionPurposeEnum]
    housing_type: Mapped[HousingTypeEnum]
    housing_area: Mapped[HousingAreaEnum]


class GuardianRequestModel(Base):
    __tablename__ = 'guardian_request'

    id: Mapped[int] = mapped_column(primary_key=True)
    request_id: Mapped[int] = mapped_column(nullable=False, unique=True)
