from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from app.models.models import BillStatus


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class BillCreate(BaseModel):
    patient_id: int = Field(..., description="Patient ID")
    appointment_id: str = Field(..., description="Appointment ID")
    consultation_fee: float = Field(..., gt=0, description="Consultation fee amount")
    medication_fee: float = Field(default=0.0, ge=0, description="Medication fee amount")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "patient_id": 1,
            "appointment_id": "APT-101",
            "consultation_fee": 1000.0,
            "medication_fee": 500.0
        }
    })


class BillResponse(BaseModel):
    bill_id: int
    patient_id: int
    appointment_id: str
    amount: float
    status: BillStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BillListResponse(BaseModel):
    bills: list[BillResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

