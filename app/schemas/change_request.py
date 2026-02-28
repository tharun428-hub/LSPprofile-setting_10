from pydantic import BaseModel


class ChangeRequestCreate(BaseModel):
    field_name: str
    new_value: str


class ChangeRequestResponse(BaseModel):
    id: int
    user_id: int
    field_name: str
    old_value: str | None
    new_value: str
    status: str

    class Config:
        orm_mode = True