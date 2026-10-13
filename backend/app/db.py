from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, List

from sqlalchemy import Column, DateTime, Float, Integer, JSON, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

Base = declarative_base()


class EventRecord(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    country = Column(String, nullable=False)
    region = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    severity = Column(Integer, nullable=False)
    summary = Column(String, nullable=False)
    metadata = Column(JSON, default=dict)
    occurred_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class StatisticRecord(Base):
    __tablename__ = "statistics"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    metric = Column(String, nullable=False)
    country = Column(String, nullable=False)
    region = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    as_of_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    source = Column(String, nullable=False)
    metadata = Column(JSON, default=dict)


engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
