from pydantic import BaseModel


class ChangeRequestCreate(BaseModel):
    request_type: str   


class ChangeRequestResponse(BaseModel):
    id: int
    user_id: int
    request_type: str
    status: str

    class Config:
        orm_mode = True