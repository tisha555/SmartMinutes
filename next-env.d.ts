# SmartMinutes - SQLAlchemy Models
# Responsibilities: Define database tables and relationships.

from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, DateTime, Text, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    meetings = relationship("Meeting", back_populates="owner", cascade="all, delete-orphan")


class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    duration = Column(Integer, nullable=False)  # in seconds
    video_url = Column(String(512), nullable=True)
    audio_url = Column(String(512), nullable=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="meetings")
    transcripts = relationship("Transcript", back_populates="meeting", cascade="all, delete-orphan")
    summary = relationship("Summary", uselist=False, back_populates="meeting", cascade="all, delete-orphan")
    action_items = relationship("ActionItem", back_populates="meeting", cascade="all, delete-orphan")


class Transcript(Base):
    __tablename__ = "transcripts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    meeting_id = Column(String(36), ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False)
    segment_index = Column(Integer, nullable=False)
    start_time = Column(Numeric(10, 3), nullable=False)
    end_time = Column(Numeric(10, 3), nullable=False)
    speaker = Column(String(100), nullable=False)
    text = Column(Text, nullable=False)
    confidence = Column(Numeric(4, 3), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    meeting = relationship("Meeting", back_populates="transcripts")


class Summary(Base):
    __tablename__ = "summaries"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    meeting_id = Column(String(36), ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False)
    executive_summary = Column(Text, nullable=False)
    topic_summary = Column(Text, nullable=False)  # Store JSON string containing topic breakdown
    key_decisions = Column(ARRAY(String), nullable=False)  # PostgreSQL array of strings or split string format
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    meeting = relationship("Meeting", back_populates="summary")


class ActionItem(Base):
    __tablename__ = "action_items"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    meeting_id = Column(String(36), ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False)
    task = Column(Text, nullable=False)
    assignee = Column(String(255), nullable=True)
    deadline = Column(String(100), nullable=True)
    status = Column(String(50), default="Pending")
    priority = Column(String(20), default="Medium")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    meeting = relationship("Meeting", back_populates="action_items")
