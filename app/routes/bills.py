from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional
import logging
import time

from app.service.database import get_db
from app.models.models import Bill, User, BillStatus
from app.utility.schemas import BillCreate, BillResponse, BillListResponse
from app.security.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/bills", tags=["bills"])


@router.post("", response_model=BillResponse, status_code=status.HTTP_201_CREATED)
async def create_bill(
    bill_data: BillCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new bill after a successful appointment.

    Calculates total amount as: (consultation_fee + medication_fee) * 1.05 (5% tax)
    """
    start_time = time.time()
    logger.info(
        f"Creating bill for patient_id={bill_data.patient_id}, "
        f"appointment_id={bill_data.appointment_id}"
    )

    try:
        # Check if bill already exists for this appointment
        existing_bill = db.query(Bill).filter(
            Bill.appointment_id == bill_data.appointment_id
        ).first()

        if existing_bill:
            logger.warning(
                f"Bill already exists for appointment_id={bill_data.appointment_id}"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Bill already exists for appointment {bill_data.appointment_id}"
            )

        # Calculate total with 5% tax
        subtotal = bill_data.consultation_fee + bill_data.medication_fee
        total_amount = subtotal * 1.05  # Adding 5% tax

        # Create new bill
        new_bill = Bill(
            patient_id=bill_data.patient_id,
            appointment_id=bill_data.appointment_id,
            amount=round(total_amount, 2),
            status=BillStatus.PENDING
        )

        db.add(new_bill)
        db.commit()
        db.refresh(new_bill)

        elapsed_time = time.time() - start_time
        logger.info(
            f"Bill created successfully: bill_id={new_bill.bill_id}, "
            f"amount={new_bill.amount}, time_taken={elapsed_time:.4f}s"
        )

        return new_bill

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating bill: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create bill"
        )


@router.get("", response_model=BillListResponse)
async def list_bills(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    patient_id: Optional[int] = Query(None, description="Filter by patient ID"),
    appointment_id: Optional[int] = Query(None, description="Filter by appointment ID"),
    status: Optional[BillStatus] = Query(None, description="Filter by bill status"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List bills with pagination and optional filters.

    Filters:
    - patient_id: Filter bills by patient
    - appointment_id: Filter bills by appointment
    - status: Filter bills by status (PENDING, PAID, CANCELLED)
    """
    start_time = time.time()
    logger.info(
        f"Listing bills: page={page}, page_size={page_size}, "
        f"patient_id={patient_id}, appointment_id={appointment_id}, status={status}"
    )

    try:
        # Build query with filters
        query = db.query(Bill)

        if patient_id is not None:
            query = query.filter(Bill.patient_id == patient_id)

        if appointment_id is not None:
            query = query.filter(Bill.appointment_id == appointment_id)

        if status is not None:
            query = query.filter(Bill.status == status)

        # Get total count
        total = query.count()

        # Apply pagination
        offset = (page - 1) * page_size
        bills = query.order_by(desc(Bill.created_at)).offset(offset).limit(page_size).all()

        # Calculate total pages
        total_pages = (total + page_size - 1) // page_size

        elapsed_time = time.time() - start_time
        logger.info(
            f"Bills retrieved: count={len(bills)}, total={total}, "
            f"time_taken={elapsed_time:.4f}s"
        )

        return BillListResponse(
            bills=bills,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    except Exception as e:
        logger.error(f"Error listing bills: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve bills"
        )


@router.get("/{bill_id}", response_model=BillResponse)
async def get_bill(
    bill_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a bill by ID"""
    start_time = time.time()
    logger.info(f"Retrieving bill: bill_id={bill_id}")

    try:
        bill = db.query(Bill).filter(Bill.bill_id == bill_id).first()

        if not bill:
            logger.warning(f"Bill not found: bill_id={bill_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bill with id {bill_id} not found"
            )

        elapsed_time = time.time() - start_time
        logger.info(
            f"Bill retrieved successfully: bill_id={bill_id}, "
            f"time_taken={elapsed_time:.4f}s"
        )

        return bill

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving bill: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve bill"
        )
# Routes module
from app.routes import bills

__all__ = ["bills"]

