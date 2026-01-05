from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from src.schemas.stats import RequestsAndDogsStatsResponse
from src.api.dependencies import SessionDep
from src.models.requests import RequestModel
from src.models.dogs import DogModel
from src.enums import RequestStatusEnum
from src.utils.auth import get_current_user
from src.utils.auth import UserModel


router = APIRouter(prefix="/stats", tags=["Stats"])


@router.get("", response_model=RequestsAndDogsStatsResponse)
async def get_count_new_requests_and_dogs(
        session: SessionDep,
        current_user: UserModel = Depends(get_current_user)):
    new_requests_result = await session.execute(
        select(func.count(RequestModel.id)).where(
            RequestStatusEnum.NEW == RequestModel.status
        )
    )
    new_requests_count = new_requests_result.scalar()

    total_dogs_result = await session.execute(
        select(func.count(DogModel.id))
    )
    total_dogs_count = total_dogs_result.scalar()

    return RequestsAndDogsStatsResponse(
        new_requests_count=new_requests_count,
        total_dogs_count=total_dogs_count
    )
