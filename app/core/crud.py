from typing import Generic, Type, TypeVar

from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import ScalarResult, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self.model: Type[ModelType] = model

    async def get_all(self, session: AsyncSession) -> list[ModelType]:
        result: ScalarResult[ModelType] = await session.scalars(select(self.model))
        return list(result.all())

    async def get_by_id(self, model_id: int, session: AsyncSession) -> ModelType | None:
        return await session.get(self.model, self.model.id == model_id)

    async def create(self, obj_in: CreateSchemaType, session: AsyncSession) -> ModelType:
        db_obj: ModelType = self.model(**obj_in.model_dump())

        session.add(db_obj)
        try:
            await session.commit()
            await session.refresh(db_obj)
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Такая запись уже существует",
            ) from e

        return db_obj

    async def update(
        self,
        obj: ModelType,
        update_obj: UpdateSchemaType,
        session: AsyncSession,
        partial: bool = False,
    ) -> ModelType:
        for key, value in update_obj.model_dump(exclude_unset=partial).items():
            setattr(obj, key, value)

        await session.commit()
        return obj

    async def remove(self, model_id: int, session: AsyncSession) -> ModelType:
        obj: ModelType | None = await session.scalar(
            select(self.model).where(self.model.id == model_id)
        )
        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__.capitalize()} with id={model_id} not found!",
            )

        await session.delete(obj)
        await session.commit()
        return obj
