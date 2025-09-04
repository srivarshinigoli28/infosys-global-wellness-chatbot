from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from . import models, schemas
from .auth import get_password_hash, verify_password, create_access_token, get_current_user

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth API", version="1.0.0")

# Allow local Streamlit app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/register", response_model=schemas.ProfileResponse, status_code=status.HTTP_201_CREATED)
def register(payload: schemas.RegisterRequest, db: Session = Depends(get_db)):
    if payload.password != payload.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    existing = db.query(models.User).filter(models.User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = models.User(
        name=payload.name.strip(),
        email=payload.email.lower(),
        hashed_password=get_password_hash(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user   # FastAPI can return SQLAlchemy object since schemas.ProfileResponse has orm_mode

@app.post("/login", response_model=schemas.TokenResponse)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/me", response_model=schemas.ProfileResponse)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user   # returns SQLAlchemy object directly

@app.put("/me", response_model=schemas.ProfileResponse)
def update_me(
    payload: schemas.ProfileUpdateRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    changed = False

    if payload.name is not None:
        current_user.name = payload.name.strip()
        changed = True
    if payload.new_password:
        current_user.hashed_password = get_password_hash(payload.new_password)
        changed = True
    if payload.age_group is not None:
        current_user.age_group = payload.age_group
        changed = True
    if payload.gender is not None:
        current_user.gender = payload.gender
        changed = True
    if payload.language is not None:
        current_user.language = payload.language
        changed = True

    if changed:
        db.add(current_user)
        db.commit()
        db.refresh(current_user)

    return current_user   # FastAPI auto-converts to ProfileResponse
