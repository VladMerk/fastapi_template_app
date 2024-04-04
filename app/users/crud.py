from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.crud import BaseCRUD
from app.users.utils import hash_password, verify_password

from .models import Users
from .schemas import UserCreate, UserUpdate


class UserCRUD(BaseCRUD[Users, UserCreate, UserUpdate]):

    async def get_by_email(self, email: str, session: AsyncSession) -> Users | None:
        return await session.scalar(select(self.model).where(self.model.email == email))

    async def create(self, obj_in: UserCreate, session: AsyncSession) -> Users:
        user = Users(email=obj_in.email, password=hash_password(obj_in.password))

        session.add(user)
        await session.commit()
        await session.flush()

        return user

    async def authenticate(self, email: str, password: str, session: AsyncSession) -> Users | None:
        user: Users | None = await self.get_by_email(email=email, session=session)

        if user is None:
            return None

        if not verify_password(plain_password=password, hashed_password=user.password):
            return None

        return user
