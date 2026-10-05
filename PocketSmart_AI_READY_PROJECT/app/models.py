from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

def now(): return datetime.now(timezone.utc)
class User(Base):
    __tablename__="users"
    id: Mapped[int]=mapped_column(primary_key=True)
    email: Mapped[str]=mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str]=mapped_column(String(120))
    password_hash: Mapped[str]=mapped_column(String(512))
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=now)
    recommendations: Mapped[list["Recommendation"]]=relationship(back_populates="user", cascade="all, delete-orphan")
class Recommendation(Base):
    __tablename__="recommendations"
    id: Mapped[int]=mapped_column(primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey("users.id"), index=True)
    planner: Mapped[str]=mapped_column(String(30), index=True)
    title: Mapped[str]=mapped_column(String(255))
    request_json: Mapped[str]=mapped_column(Text)
    response_json: Mapped[str]=mapped_column(Text)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=now)
    user: Mapped[User]=relationship(back_populates="recommendations")
