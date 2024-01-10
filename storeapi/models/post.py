from pydantic import BaseModel, ConfigDict


class UserPostIn(BaseModel):
    body: str


class UserPostOut(UserPostIn):
    id: int
    model_config = ConfigDict(from_attributes=True)


class CommentIn(BaseModel):
    body: str
    post_id: int


class CommentOut(CommentIn):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserPostWithComments(BaseModel):
    post: UserPostOut
    comments: list[CommentOut]
