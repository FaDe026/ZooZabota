from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.api.dependencies import SessionDep
from src.models.requests import RequestModel, AdoptionRequestModel, GuardianRequestModel
from src.schemas.requests import RequestCreateSchema, RequestResponseSchema
from src.enums import RequestTypeEnum

router = APIRouter(prefix="/requests", tags=["Requests"])


@router.post("", response_model=RequestResponseSchema)
async def create_request(request_data: RequestCreateSchema, session: SessionDep):
    request = RequestModel(
        dog_id=request_data.dog_id,
        full_name=request_data.full_name,
        phone=request_data.phone,
        email=request_data.email,
        status=request_data.status,
        type=request_data.type
    )
    session.add(request)
    await session.flush()

    if request_data.type == RequestTypeEnum.ADOPTION_REQUEST:
        adoption = AdoptionRequestModel(
            request_id=request.id,
            **request_data.adoption_details.model_dump()
        )
        session.add(adoption)
    elif request_data.type == RequestTypeEnum.GUARDIAN_REQUEST:
        guardian = GuardianRequestModel(request_id=request.id)
        session.add(guardian)

    await session.commit()

    result = await session.execute(
        select(RequestModel)
        .options(
            selectinload(RequestModel.adoption_request),
            selectinload(RequestModel.guardian_request)
        )
        .where(request.id == RequestModel.id)
    )
    full_request = result.scalar_one()
    return full_request

@router.get("", response_model=list[RequestResponseSchema])
async def get_requests(session: SessionDep):
    query = (select(RequestModel).options(selectinload(RequestModel.adoption_request),selectinload(RequestModel.guardian_request)))
    result = await session.execute(query)
    return result.scalars().all()

@router.get("/{request_id}", response_model=RequestResponseSchema)
async def get_request(request_id: int, session: SessionDep):
    query = (
        select(RequestModel)
        .options(
            selectinload(RequestModel.adoption_request),
            selectinload(RequestModel.guardian_request)
        )
        .where(request_id == RequestModel.id)
    )
    result = await session.execute(query)
    request = result.scalar_one_or_none()
    if request is None:
        raise HTTPException(404, "Заявка не найдена")
    return request