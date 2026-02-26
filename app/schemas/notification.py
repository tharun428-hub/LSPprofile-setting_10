from pydantic import BaseModel



class NotificationBase(BaseModel):
    sms: bool
    email: bool
    loan_updates: bool
    emi_reminders: bool
    payment_alerts: bool
    push_notification: bool



class NotificationUpdate(NotificationBase):
    pass



class NotificationResponse(NotificationBase):
    user_id: int

    class Config:
        from_attributes = True
