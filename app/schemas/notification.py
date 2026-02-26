from pydantic import BaseModel


# BASE SCHEMA (MUST COME FIRST)
class NotificationBase(BaseModel):
    sms: bool
    email: bool
    loan_updates: bool
    emi_reminders: bool
    payment_alerts: bool
    push_notification: bool


# UPDATE SCHEMA
class NotificationUpdate(NotificationBase):
    pass


# RESPONSE SCHEMA
class NotificationResponse(NotificationBase):
    user_id: int

    class Config:
        from_attributes = True
