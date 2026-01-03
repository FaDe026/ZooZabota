from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.api.dependencies import SessionDep
from src.models.requests import RequestModel, AdoptionRequestModel, GuardianRequestModel
from src.schemas.requests import RequestCreateSchema, RequestResponseSchema, RequestPatchSchema
from src.enums import RequestTypeEnum
from src.enums import RequestStatusEnum
from src.utils.auth import UserModel
from src.utils.auth import get_current_user

router = APIRouter(prefix="/requests", tags=["Requests"])


@router.post("", response_model=RequestResponseSchema)
async def create_request(request_data: RequestCreateSchema, session: SessionDep, current_user: UserModel = Depends(get_current_user)):
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

@router.put("/{request_id}", response_model=RequestResponseSchema)
async def update_request(request_id: int, request_data: RequestCreateSchema, session: SessionDep, current_user: UserModel = Depends(get_current_user)):
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

    if request.type != request_data.type:
        if request.adoption_request:
            await session.delete(request.adoption_request)
            request.adoption_request = None
        elif request.guardian_request:
            await session.delete(request.guardian_request)
            request.guardian_request = None

    for key, value in request_data.model_dump(exclude={"adoption_details", "guardian_details"}).items():
        setattr(request, key, value)

    if request_data.type == RequestTypeEnum.ADOPTION_REQUEST:
        if request.adoption_request:
            for key, value in request_data.adoption_details.model_dump().items():
                setattr(request.adoption_request, key, value)
        else:
            adoption = AdoptionRequestModel(
                request_id=request.id,
                **request_data.adoption_details.model_dump()
            )
            session.add(adoption)
    elif request_data.type == RequestTypeEnum.GUARDIAN_REQUEST:
        if not request.guardian_request:
            guardian = GuardianRequestModel(request_id=request.id)
            session.add(guardian)

    await session.commit()
    await session.refresh(request)

    result = await session.execute(
        select(RequestModel)
        .options(
            selectinload(RequestModel.adoption_request),
            selectinload(RequestModel.guardian_request)
        )
        .where(RequestModel.id == request.id)
    )
    return result.scalar_one()


@router.patch("/{request_id}", response_model=RequestResponseSchema)
async def partial_update_request(request_id: int, update_data: RequestPatchSchema,session: SessionDep, current_user: UserModel = Depends(get_current_user)):
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

    if update_data.type is not None and update_data.type != request.type:
        if request.adoption_request:
            await session.delete(request.adoption_request)
        if request.guardian_request:
            await session.delete(request.guardian_request)

        if update_data.type == RequestTypeEnum.ADOPTION_REQUEST:
            adoption = AdoptionRequestModel(request_id=request.id)
            session.add(adoption)
        elif update_data.type == RequestTypeEnum.GUARDIAN_REQUEST:
            guardian = GuardianRequestModel(request_id=request.id)
            session.add(guardian)

        request.type = update_data.type

    for field, value in update_data.model_dump(exclude_unset=True).items():
        if field == "adoption_details":
            continue
        setattr(request, field, value)

    if request.type == RequestTypeEnum.ADOPTION_REQUEST and update_data.adoption_details is not None and request.adoption_request:
        for field, value in update_data.adoption_details.model_dump().items():
            setattr(request.adoption_request, field, value)

    await session.commit()
    await session.refresh(request)

    result = await session.execute(
        select(RequestModel)
        .options(
            selectinload(RequestModel.adoption_request),
            selectinload(RequestModel.guardian_request)
        )
        .where(request_id == RequestModel.id)
    )
    return result.scalar_one()


@router.delete("/{request_id}")
async def delete_request(request_id: int, session: SessionDep, current_user: UserModel = Depends(get_current_user)):
    request = await session.get(RequestModel, request_id)
    if request is None:
        raise HTTPException(404, "Заявка не найдена")
    await session.delete(request)
    await session.commit()
    return {"message": f"Заявка {request_id} успешно удалена"}