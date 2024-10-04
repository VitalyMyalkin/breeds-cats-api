from contextlib import asynccontextmanager
from fastapi import FastAPI, status

from database.database import create_tables, delete_tables
from repository.repository import CatRepository, BreedSchema, CatSchema


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("База готова")
    yield
    await delete_tables()
    print("База очищена")


app = FastAPI(lifespan=lifespan)


@app.post("/cat", status_code=status.HTTP_201_CREATED)
async def add_cat(payload: CatSchema):
    new_cat = await CatRepository.add_cat(payload)
    return new_cat


@app.post("/breed", status_code=status.HTTP_201_CREATED)
async def add_breed(payload: BreedSchema):
    new_breed = await CatRepository.add_breed(payload)
    return new_breed


@app.get("/cats", status_code=status.HTTP_200_OK)
async def get_cats():
    cats = await CatRepository.get_cats()
    return cats


@app.get("/breeds", status_code=status.HTTP_200_OK)
async def get_breeds():
    breeds = await CatRepository.get_breeds()
    return breeds


@app.get("/cat/{cat_id}", status_code=status.HTTP_200_OK)
async def get_cat(cat_id: int):
    cat = await CatRepository.get_cat(cat_id)
    return cat


@app.put("/cat/{cat_id}", status_code=status.HTTP_200_OK)
async def update_cat(cat_id: int, payload: CatSchema):
    cat = await CatRepository.update_cat(cat_id, payload)
    return cat


@app.delete("/cat/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cat(cat_id: int):
    result = await CatRepository.delete_cat(cat_id)
    return result


@app.get("/cats-filter/{breed_name}", status_code=status.HTTP_200_OK)
async def get_cats_by_breed(breed_name: str):
    cats = await CatRepository.get_cats_by_breed(breed_name)
    return cats
