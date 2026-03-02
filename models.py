from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    role = Column(String)  # admin, mesario, pais
    is_active = Column(Boolean, default=True)
    
    # Relationships
    matches = relationship("Match", back_populates="user")

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    date = Column(String, nullable=False)
    status = Column(String, default="agendado")  # agendado, em_andamento, finalizado
    home_score = Column(Integer, default=0)
    away_score = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    user = relationship("User", back_populates="matches")
    events = relationship("MatchEvent", back_populates="match")

class MatchEvent(Base):
    __tablename__ = "match_events"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"))
    type = Column(String, nullable=False)  # goal, yellow_card, red_card, start, end
    team = Column(String, nullable=False)  # home, away, system
    description = Column(String, nullable=False)
    timestamp = Column(String, nullable=False)
    
    # Relationships
    match = relationship("Match", back_populates="events")
