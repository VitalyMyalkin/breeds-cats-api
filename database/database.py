from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config import get_db_url

DATABASE_URL = get_db_url()

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
# создали асинхронный движок, его будем использовать для походов в постгрес
Base = declarative_base()


class Breed(Base):
    """
    Класс Порода

    Для создания таблицы в постгрес
    """
    __tablename__ = 'breeds'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    cats = relationship('Cat', back_populates='breeds')

    def __str__(self):
        return self.name


class Cat(Base):
    """
    Класс Котята

    Для создания таблицы в постгрес.
    """
    __tablename__ = 'cats'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), index=True, nullable=False)
    COLOR_CHOICES = Enum('multicolored', 'white', 'brown', 'red', 'black', 'grey', name='color')
    color = Column(COLOR_CHOICES, default='multicolored', nullable=False)
    age = Column(Integer, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    breed_id = Column(Integer, ForeignKey('breeds.id'))
    breeds = relationship('Breed', back_populates='cats')

    def __str__(self):
        return self.name


async def create_tables():
    """Миграция асинхронно"""
    async with engine.begin() as conn:
        await conn.run_sync(Breed.metadata.create_all)
        await conn.run_sync(Cat.metadata.create_all)


async def delete_tables():
    """Очищаем базу асинхронно"""
    async with engine.begin() as conn:
        await conn.run_sync(Breed.metadata.drop_all)
        await conn.run_sync(Cat.metadata.drop_all)
