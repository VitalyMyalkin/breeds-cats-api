from sqlalchemy import select
from sqlalchemy.orm import joinedload
from fastapi import HTTPException
from pydantic import BaseModel, Field, ConfigDict

from database.database import async_session_maker, Cat, Breed


class BreedSchema(BaseModel):
    """
    Схема породы Pydantic.

    Для валидации входящих данных, возможно для вывода ответов API
    """
    name: str = Field(..., min_length=1, max_length=255)
    model_config = ConfigDict(from_attributes=True)


class CatSchema(BaseModel):
    """
    Схема котенка Pydantic.

    Для валидации входящих данных, возможно для вывода ответов API
    """
    name: str = Field(..., min_length=1, max_length=255)
    color: str = Field(..., min_length=1, max_length=50)
    description: str = Field(..., min_length=1, max_length=1000)
    age: int = Field(..., ge=0)
    # потому что котенку может быть 4 дня и 0 полных месяцев
    breed_id: int
    model_config = ConfigDict(from_attributes=True)


class CatRepository:
    @classmethod
    async def add_cat(cls, payload) -> Cat:
        """
        Добавляет котенка в базу.

        Если айдишника породы нет, то выбрасывает исключение.
        Возвращает котенка с айдишником и датой добавления
        """
        new_cat = Cat(**payload.dict())
        async with async_session_maker() as session:
            result = await session.execute(select(Breed).where(Breed.id == payload.breed_id))
            obj = result.scalar()
            if not obj:
                raise HTTPException(status_code=404, detail="Breed not found")
            session.add(new_cat)
            await session.flush()
            await session.commit()
            return new_cat

    @classmethod
    async def add_breed(cls, payload) -> Breed:
        """
        Добавляет новую породу в базу.

        Возвращает породу с айдишником и датой добавления
        """
        new_breed = Breed(**payload.dict())

        async with async_session_maker() as session:
            session.add(new_breed)
            await session.flush()
            await session.commit()
            return new_breed

    @classmethod
    async def get_cats(cls) -> list[dict]:
        """
        Получение списка всех котят.

        Информация о них максимально полная
        """
        async with async_session_maker() as session:
            result = await session.execute(select(Cat).options(joinedload(Cat.breeds)))
            data = result.scalars().all()
            cats = []
            for cat in data:
                cats.append(
                    {"id": cat.id,
                     "name": cat.name,
                     "color": cat.color,
                     "description": cat.description,
                     "age": cat.age,
                     "breed": cat.breeds.name,
                     "breed_id": cat.breed_id
                     }
                )
            return cats

    @classmethod
    async def get_breeds(cls) -> list[BreedSchema]:
        """
        Получение списка всех пород
        """
        async with async_session_maker() as session:
            result = await session.execute(select(Breed))
            data = result.scalars().all()
            breeds = [BreedSchema.model_validate(breed) for breed in data]
            return breeds

    @classmethod
    async def update_cat(cls, cat_id: int, payload: CatSchema) -> Cat:
        """
        Изменяет данные котенка, хранящиеся в базе.

        Если такого котенка в базе нет - выбросит исключение
        """
        async with async_session_maker() as session:
            result = await session.execute(select(Cat).options(joinedload(Cat.breeds)).where(Cat.id == cat_id))
            objcat = result.scalar()
            if not objcat:
                raise HTTPException(status_code=404, detail="Cat not found")
            for key, value in payload.dict().items():
                setattr(objcat, key, value)
            result = await session.execute(select(Breed).where(Breed.id == payload.breed_id))
            objbreed = result.scalar()
            if not objbreed:
                raise HTTPException(status_code=404, detail="Breed not found")
            await session.commit()
            return objcat

    @classmethod
    async def delete_cat(cls, cat_id: int):
        """
        Удаляет котенка из базы по айдишнику.

        Если такого айдишника в базе нет - выбросит исключение
        """
        async with async_session_maker() as session:
            result = await session.execute(select(Cat).where(Cat.id == cat_id))
            obj = result.scalar()
            if not obj:
                raise HTTPException(status_code=404, detail="Cat not found")
            await session.delete(obj)
            await session.commit()
            return "Cat deleted successfully"

    @classmethod
    async def get_cat(cls, cat_id: int) -> dict:
        """
        Получение макисмально полной информации о котенке по айдишнику

        Если такого айдишника в базе нет - выбросит исключение
        """
        async with async_session_maker() as session:
            result = await session.execute(select(Cat).options(joinedload(Cat.breeds)).where(Cat.id == cat_id))
            obj = result.scalar()
            if not obj:
                raise HTTPException(status_code=404, detail="Cat not found")
            return {"id": obj.id,
                    "name": obj.name,
                    "color": obj.color,
                    "description": obj.description,
                    "age": obj.age,
                    "breed": obj.breeds.name,
                    "breed_id": obj.breed_id
                    }

    @classmethod
    async def get_cats_by_breed(cls, breed_name: str) -> list[dict]:
        """
        Получение списка котят определенной породы.

        Если такой породы в базе нет - выбросит исключение
        """
        async with async_session_maker() as session:
            result = await session.execute(select(Breed).where(Breed.name == breed_name))
            obj = result.scalar()
            if not obj:
                raise HTTPException(status_code=404, detail="Breed not found")
            result = await session.execute(select(Cat).filter(Cat.breed_id == obj.id).options(joinedload(Cat.breeds)))
            data = result.scalars().all()
            cats = []
            for cat in data:
                cats.append(
                    {"id": cat.id,
                     "name": cat.name,
                     "color": cat.color,
                     "description": cat.description,
                     "age": cat.age,
                     "breed": cat.breeds.name,
                     "breed_id": cat.breed_id
                     }
                )
            return cats
