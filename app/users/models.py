from typing import TYPE_CHECKING

from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.database import Base

if TYPE_CHECKING:
    # Убирает предупреждения отсутствия импорта и неприятные подчеркивания в 
    # PyCharm и VSCode
    from bookings.models import Bookings


# Модель написана в соответствии с современным стилем Алхимии (версии 2.x)
class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    hashed_password: Mapped[str]

    bookings: Mapped[list["Bookings"]] = relationship(back_populates="user")

    def __str__(self):
        return f"Пользователь {self.email}"

# Модель написана в соответствии со старым стилем Алхимии (версии 1.x)
# class Users(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True)
#     email = Column(String, nullable=False)
#     hashed_password = Column(String, nullable=False)

#     bookings = relationship("Bookings", back_populates="user")

#     def __str__(self):
#         return f"Пользователь {self.email}"
