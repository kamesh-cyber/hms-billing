from sqlalchemy.orm import Session
from app.models.models import Bill, User, BillStatus
from app.security.auth import get_password_hash
from datetime import datetime
import logging
import csv
import os

logger = logging.getLogger(__name__)


def seed_users(db: Session):
    """Seed users table with default users"""
    try:
        existing_users = db.query(User).count()
        if existing_users == 0:
            logger.info("Seeding users...")
            users = [
                User(username="admin", hashed_password=get_password_hash("admin123")),
                User(username="billing_user", hashed_password=get_password_hash("billing123")),
            ]
            db.add_all(users)
            db.commit()
            logger.info(f"Seeded {len(users)} users successfully")
        else:
            logger.info("Users already exist, skipping user seeding")
    except Exception as e:
        logger.error(f"Error seeding users: {str(e)}")
        db.rollback()
        raise


def seed_bills_from_csv(db: Session):
    """Seed bills table from CSV file"""
    try:
        existing_bills = db.query(Bill).count()
        if existing_bills > 0:
            logger.info("Bills already exist, skipping bill seeding")
            return

        # Get the path to the CSV file
        csv_path = os.path.join(
            os.path.dirname(__file__),
            "resources",
            "hms_bills.csv"
        )

        if not os.path.exists(csv_path):
            logger.warning(f"CSV file not found at {csv_path}, skipping bill seeding")
            return

        logger.info(f"Loading bills from CSV: {csv_path}")

        bills = []
        with open(csv_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Map CSV status to our BillStatus enum
                csv_status = row['status'].upper()
                if csv_status == 'OPEN':
                    bill_status = BillStatus.PENDING
                elif csv_status == 'VOID':
                    bill_status = BillStatus.CANCELLED
                else:  # PAID
                    bill_status = BillStatus.PAID

                # Parse the datetime
                created_at = datetime.strptime(row['created_at'], '%Y-%m-%d %H:%M:%S')

                bill = Bill(
                    bill_id=int(row['bill_id']),
                    patient_id=int(row['patient_id']),
                    appointment_id=row['appointment_id'],
                    amount=float(row['amount']),
                    status=bill_status,
                    created_at=created_at
                )
                bills.append(bill)

        # Bulk insert bills
        db.bulk_save_objects(bills)
        db.commit()
        logger.info(f"Seeded {len(bills)} bills from CSV successfully")

    except Exception as e:
        logger.error(f"Error seeding bills from CSV: {str(e)}")
        db.rollback()
        raise


def seed_database(db: Session):
    """Seed the database with initial data"""
    logger.info("Starting database seeding...")
    seed_users(db)
    seed_bills_from_csv(db)
    logger.info("Database seeding completed")


