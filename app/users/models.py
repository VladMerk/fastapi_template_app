from sqlalchemy import BLOB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class Users(Base):
    __tablename__: str = "users"

    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes] = mapped_column(BLOB, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
