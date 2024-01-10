# conda activate envFastApi
# uvicorn storeapi.main:app --reload

from contextlib import asynccontextmanager

from fastapi import FastAPI
from storeapi.database import database
from storeapi.routers.post import router as post_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    A context manager is basically a function that does some setup and some teardown, and returns a value.
    In the middle it pauses execution until somthing happens.
    1) runs the setup code - database.connect()
    2) stops running until FastAPI tells it to continue
    3) runs the teardown code - database.disconnect()
    We are running the function before the app is ready to respond to requests.
    Then the function stops and FastApi is going to leave it there until the app is shutting down (e.g. when we terminate the app).
    It then the app is going to run the rest of the function - execute the teardown code.
    Events from previous versions of FastAPI are still available, but this is the recoomended way to do it.
    """
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(post_router)

# app.include_router(post_router, prefix="/posts")

# post_table = {}


@app.get("/")
async def root():
    return {
        "message": "Hello world!",
    }


# @app.post("/post", response_model=UserPostOut)
# async def create_post(user_post: UserPostIn):
#     data = user_post.dict()
#     last_record_id = len(post_table)
#     new_post = {**data, "id": last_record_id}
#     post_table[last_record_id] = new_post
#     return new_post


# # async def create_post(user_post: UserPostIn):
# #     post_id = len(post_table) + 1
# #     post_table[post_id] = user_post
# #     return UserPostOut(**user_post.dict(), id=post_id)


# @app.get("/post", response_model=list[UserPostOut])
# async def get_all_posts():
#     return list(post_table.values())
