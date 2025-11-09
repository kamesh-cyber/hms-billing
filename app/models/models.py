from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import validates
from app.service.database import Base
import enum


class BillStatus(str, enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    CANCELLED = "CANCELLED"


class Bill(Base):
    __tablename__ = "bills"

    bill_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(Integer, nullable=False, index=True)
    appointment_id = Column(String(100), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    status = Column(Enum(BillStatus), default=BillStatus.PENDING, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    @validates('appointment_id')
    def validate_appointment_id(self, key, value):
        """Ensure appointment_id is always stored as string, converting from int if needed"""
        if value is not None and isinstance(value, int):
            return str(value)
        return value


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)

