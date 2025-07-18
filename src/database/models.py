from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey


class Base(DeclarativeBase):
    pass


class Text(Base):
    """
    Основная модель для данных моделей текстовых
    """

    __tablename__ = "text"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column(String, nullable=False)
    user_rel = relationship("User", back_populates="text_rel")


class Monitor(Base):
    """
    Модель дляхранения данных моделей разрешений
    """

    __tablename__ = "monitor"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    width: Mapped[int] = mapped_column(Integer, nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
    user_rel = relationship("User", back_populates="monitor_rel")


class Picture(Base):
    """
    Модель для данных моделей генерирующих картинки
    """

    __tablename__ = "picture"
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column(String, nullable=False)
    user_rel = relationship("User", back_populates="picture_rel")


class User(Base):
    """
    Модель для пользователя
    """

    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    tel_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    text: Mapped[int] = mapped_column(
        ForeignKey("text.id", ondelete="CASCADE"), nullable=True
    )
    monitor: Mapped[int] = mapped_column(
        ForeignKey("monitor.id", ondelete="CASCADE"), nullable=True
    )
    picture: Mapped[int] = mapped_column(
        ForeignKey("picture.id", ondelete="CASCADE"), nullable=True
    )

    text_rel = relationship("Text", back_populates="user_rel")
    monitor_rel = relationship("Monitor", back_populates="user_rel")
    picture_rel = relationship("Picture", back_populates="user_rel")
