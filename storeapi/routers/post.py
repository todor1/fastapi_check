### APIRouter: basically a mini FastAPI app that can be included into an existing FastAPI app

from fastapi import APIRouter, HTTPException
from storeapi.database import comment_table, database, post_table
from storeapi.models.post import (
    CommentIn,
    CommentOut,
    UserPostIn,
    UserPostOut,
    UserPostWithComments,
)

# from pydantic_settings import BaseSettings, SettingsConfigDict


router = APIRouter()


async def find_post(post_id: int):
    query = post_table.select().where(post_table.c.id == post_id)
    ### get the first record that matches the query
    return await database.fetch_one(query)


@router.post("/post", response_model=UserPostOut, status_code=201)
async def create_post(user_post: UserPostIn):
    data = user_post.model_dump()
    query = post_table.insert().values(data)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


@router.get("/post", response_model=list[UserPostOut])
async def get_all_posts():
    query = post_table.select()
    return await database.fetch_all(query)


@router.post("/comment", response_model=CommentOut, status_code=201)
async def create_comment(comment: CommentIn):
    post = await find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    data = comment.model_dump()
    query = comment_table.insert().values(data)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


@router.get("/post/{post_id}/comment", response_model=list[CommentOut])
async def get_comments_on_post(post_id: int):
    query = comment_table.select().where(comment_table.c.post_id == post_id)
    return await database.fetch_all(query)


@router.get("/post/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):
    post = await find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {
        "post": post,
        "comments": await get_comments_on_post(post_id),
    }
