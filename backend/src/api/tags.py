from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from src.api.dependencies import SessionDep
from src.models.tags import TagModel
from src.schemas.tags import TagAddSchema, TagResponseSchema
from src.utils.auth import UserModel
from src.utils.auth import get_current_user


router = APIRouter(prefix="/tags", tags=["Tags"])


@router.post("", response_model=TagResponseSchema)
async def add_tag(data: TagAddSchema,
                  session: SessionDep,
                  current_user: UserModel = Depends(get_current_user)):
    new_tag = TagModel(name=data.name)
    session.add(new_tag)
    await session.commit()
    return new_tag


@router.get("", response_model=list[TagResponseSchema])
async def get_tags(session: SessionDep):
    query = select(TagModel)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/{tag_id}", response_model=TagResponseSchema)
async def get_tag(tag_id: int, session: SessionDep):
    query = select(TagModel).where(tag_id == TagModel.id)
    result = await session.execute(query)
    tag = result.scalar_one_or_none()
    if tag is None:
        raise HTTPException(
            status_code=404,
            detail="Информация о теге не найдена"
        )
    return tag


@router.put("/{tag_id}", response_model=TagResponseSchema)
async def put_tag(tag_id: int,
                  data: TagAddSchema,
                  session: SessionDep,
                  current_user: UserModel = Depends(get_current_user)):
    query = select(TagModel).where(tag_id == TagModel.id)
    result = await session.execute(query)
    tag = result.scalar_one_or_none()
    if tag is None:
        raise HTTPException(
            status_code=404,
            detail="Информация о теге не найдена"
        )
    tag.name = data.name
    session.add(tag)
    await session.commit()
    await session.refresh(tag)
    return tag


@router.patch("/{tag_id}", response_model=TagResponseSchema)
async def partial_update_tag(tag_id: int,
                             data: TagAddSchema,
                             session: SessionDep,
                             current_user: UserModel = Depends(get_current_user)):
    query = select(TagModel).where(tag_id == TagModel.id)
    result = await session.execute(query)
    tag = result.scalar_one_or_none()
    if tag is None:
        raise HTTPException(
            status_code=404,
            detail="Информация о теге не найдена"
        )
    update_dict = data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(tag, key, value)
    session.add(tag)
    await session.commit()
    await session.refresh(tag)
    return tag


@router.delete("/{tag_id}", response_model=TagResponseSchema)
async def delete_tag(tag_id: int,
                     session: SessionDep,
                     current_user: UserModel = Depends(get_current_user)):
    query = select(TagModel).where(tag_id == TagModel.id)
    result = await session.execute(query)
    tag = result.scalar_one_or_none()
    if tag is None:
        raise HTTPException(
            status_code=404,
            detail="Информация о теге не найдена"
        )
    await session.delete(tag)
    await session.commit()
    return tag
