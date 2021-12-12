from fastapi import FastAPI
from pydantic import BaseSettings

from backend.app.database.db import SessionLocal, engine, Base
from backend.app.routers import images, users, items, category, auth

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def read():
    return {"Hello": "World"}


@app.get("/hello")
def hello():
    return {"I said": "Hello"}


app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(items.router, prefix="/items", tags=["items"])
app.include_router(category.router, prefix="/category", tags=["category"])
app.include_router(images.router, prefix="/images", tags=["images"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
