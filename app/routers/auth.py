from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from datetime import timedelta

from ..database import get_session
from ..models import User
from ..schemas import UserResponse, UserCreate, Token
from ..auth import (
    get_password_hash,
    verify_password, 
    create_access_token, 
    oauth2_scheme,
    verify_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/auth", tags=["auth"])

#Registrar um novo usuário
@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, session: Session = Depends(get_session)):

    existing_user = session.exec(
        select(User)
        .where(
            (User.email == user.email) | (User.username == user.username)
        )).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username alredy registered"
        )
    
    hashed_password = get_password_hash(user.password)

    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

#Efetua login
@router.post("/login", response_model=Token)
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: Session = Depends(get_session)
    ):
    
    user = session.exec(
        select(User).where(User.username == form_data.username)
    ).first()

    if not user or not verify_password(form_data.password , user.hashed_password):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect password or username',
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expire
    )

    return {"access_token": access_token, "token_type": "bearer"}

#Verifica Token atual
@router.get("/verify")
def verify_token_endpoint(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    return {"valid": True, "username": payload.get("sub")}