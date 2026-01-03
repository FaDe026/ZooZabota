from __future__ import annotations
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from src.database import Base
from src.enums import (RequestStatusEnum, FamilyMemberCountEnum,
                       PetExperienceEnum, AdoptionPurposeEnum,
                       HousingTypeEnum, HousingAreaEnum,
                       RequestTypeEnum)

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

    adoption_request: Mapped[Optional["AdoptionRequestModel"]] = relationship(
        back_populates="request", cascade="all, delete-orphan"
    )
    guardian_request: Mapped[Optional["GuardianRequestModel"]] = relationship(
        back_populates="request", cascade="all, delete-orphan"
    )


class AdoptionRequestModel(Base):
    __tablename__ = 'adoption_request'

    id: Mapped[int] = mapped_column(primary_key=True)
    request_id: Mapped[int] = mapped_column(
        ForeignKey("request.id"),
        nullable=False,
        unique=True
    )

    family_member_count: Mapped[FamilyMemberCountEnum]
    had_experience_adoption_pet: Mapped[PetExperienceEnum]
    adoption_purpose: Mapped[AdoptionPurposeEnum]
    housing_type: Mapped[HousingTypeEnum]
    housing_area: Mapped[HousingAreaEnum]

    request: Mapped["RequestModel"] = relationship(
        back_populates="adoption_request"
    )


class GuardianRequestModel(Base):
    __tablename__ = 'guardian_request'

    id: Mapped[int] = mapped_column(primary_key=True)
    request_id: Mapped[int] = mapped_column(
        ForeignKey("request.id"),
        nullable=False,
        unique=True
    )

    request: Mapped["RequestModel"] = relationship(
        back_populates="guardian_request"
    )
