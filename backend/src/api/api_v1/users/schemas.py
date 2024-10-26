from pydantic import BaseModel, ConfigDict


class CreateUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    hashed_password: str


class ValidateUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    hashed_password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    hashed_password: str
    active: bool
