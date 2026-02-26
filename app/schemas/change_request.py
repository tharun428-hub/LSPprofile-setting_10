from pydantic import BaseModel


class ChangeRequestCreate(BaseModel):
    request_type: str   # lock or delete


class ChangeRequestResponse(BaseModel):
    id: int
    user_id: int
    request_type: str
    status: str

    class Config:
        orm_mode = True