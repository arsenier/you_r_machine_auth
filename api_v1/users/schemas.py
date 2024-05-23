from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


# class UserUpdate(UserCreate):
#     pass


class UserUpdatePartial(UserCreate):
    username: None


class UserSchema(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
