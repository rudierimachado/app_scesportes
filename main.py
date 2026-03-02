from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import List

import models, schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Arquibancada Digital API")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": user.email, "token_type": "bearer"}

# User endpoints
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password, full_name=user.full_name, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.password:
        db_user.hashed_password = get_password_hash(user.password)
    db_user.email = user.email
    db_user.full_name = user.full_name
    db_user.role = user.role
    
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

# Match endpoints
@app.post("/matches/", response_model=schemas.Match)
def create_match(match: schemas.MatchCreate, db: Session = Depends(get_db)):
    db_match = models.Match(**match.dict())
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match

@app.get("/matches/", response_model=List[schemas.Match])
def read_matches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    matches = db.query(models.Match).offset(skip).limit(limit).all()
    return matches

@app.get("/matches/{match_id}", response_model=schemas.Match)
def read_match(match_id: int, db: Session = Depends(get_db)):
    db_match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return db_match

@app.put("/matches/{match_id}", response_model=schemas.Match)
def update_match(match_id: int, match: schemas.MatchCreate, db: Session = Depends(get_db)):
    db_match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    
    for key, value in match.dict().items():
        setattr(db_match, key, value)
    
    db.commit()
    db.refresh(db_match)
    return db_match

@app.delete("/matches/{match_id}")
def delete_match(match_id: int, db: Session = Depends(get_db)):
    db_match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    db.delete(db_match)
    db.commit()
    return {"message": "Match deleted successfully"}

# Match Event endpoints
@app.post("/events/", response_model=schemas.MatchEvent)
def create_event(event: schemas.MatchEventCreate, db: Session = Depends(get_db)):
    db_event = models.MatchEvent(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@app.get("/matches/{match_id}/events", response_model=List[schemas.MatchEvent])
def read_match_events(match_id: int, db: Session = Depends(get_db)):
    events = db.query(models.MatchEvent).filter(models.MatchEvent.match_id == match_id).all()
    return events

@app.delete("/events/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    db_event = db.query(models.MatchEvent).filter(models.MatchEvent.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(db_event)
    db.commit()
    return {"message": "Event deleted successfully"}

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao Backend do Arquibancada Digital"}
