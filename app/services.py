
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Registration
from app.schemas import RegistrationCreate

EVENT_CAPACITY = 50


def create_registration(
    db: Session,
    registration_data: RegistrationCreate,
) -> Registration:
    # Check whether this email is already registered.
    existing = db.scalar(
        select(Registration.id).where(
            func.lower(Registration.email)
            == registration_data.email.lower()
        )
    )

    if existing is not None:
        raise ValueError("This email is already registered.")

    # Check whether the event has reached capacity.
    count = db.scalar(
        select(func.count()).select_from(Registration)
    ) or 0

    if count >= EVENT_CAPACITY:
        raise OverflowError("Event registration is full.")

    # Create the new registration.
    registration = Registration(
        name=registration_data.name.strip(),
        email=str(registration_data.email).lower(),
        college=registration_data.college,
        department=registration_data.department,
    )

    db.add(registration)

    try:
        db.commit()
        db.refresh(registration)
    except IntegrityError:
        # A concurrent request might have registered this email first.
        db.rollback()
        raise ValueError("This email is already registered.") from None

    return registration
