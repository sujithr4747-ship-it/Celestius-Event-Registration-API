
from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Registration
from app.schemas import RegistrationCreate, RegistrationResponse
from app.services import create_registration

# Create the database tables when the application starts.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Celestius Event Registration API",
    description="Backend API for the Celestius Backend Development Workshop.",
    version="1.0.0",
)


@app.get("/")
def home():
    return {"message": "Celestius Registration API is running"}


@app.post(
    "/register",
    response_model=RegistrationResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_participant(
    registration_data: RegistrationCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_registration(db, registration_data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except OverflowError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@app.get("/registrations", response_model=list[RegistrationResponse])
def list_registrations(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    statement = (
        select(Registration)
        .order_by(Registration.id)
        .offset(skip)
        .limit(limit)
    )
    return db.scalars(statement).all()


@app.get(
    "/registrations/{registration_id}",
    response_model=RegistrationResponse,
)
def get_registration(
    registration_id: int,
    db: Session = Depends(get_db),
):
    registration = db.get(Registration, registration_id)

    if registration is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found.",
        )

    return registration
