from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class Users(Base):
    __tablename__: str = "users"

    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
