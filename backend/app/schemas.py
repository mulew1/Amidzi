from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class EventPayload(BaseModel):
    source: str
    topic: str
    event_type: str
    country: str
    region: str
    latitude: float
    longitude: float
    severity: int = Field(ge=1, le=10)
    summary: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class StatisticPayload(BaseModel):
    metric: str
    country: str
    region: str
    value: float
    unit: str
    source: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class FilterQuery(BaseModel):
    country: Optional[str] = None
    region: Optional[str] = None
    topic: Optional[str] = None
    event_type: Optional[str] = None
    limit: int = 20
