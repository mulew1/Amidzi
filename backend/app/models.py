from __future__ import annotations

from datetime import datetime, timedelta
from typing import List

from sqlalchemy import select

from app.db import EventRecord, SessionLocal, StatisticRecord

SEED_EVENTS = [
    {
        "source": "GDELT",
        "topic": "conflict",
        "event_type": "military action",
        "country": "Ukraine",
        "region": "Europe",
        "latitude": 49.0,
        "longitude": 32.0,
        "severity": 9,
        "summary": "Regional security alerts rise after increased military activity near key transit corridors.",
        "metadata": {"impact": "high", "sentiment": "volatile"},
        "occurred_at": datetime.utcnow() - timedelta(hours=1),
    },
    {
        "source": "ACLED",
        "topic": "protest",
        "event_type": "civil unrest",
        "country": "Kenya",
        "region": "Africa",
        "latitude": -1.29,
        "longitude": 36.82,
        "severity": 7,
        "summary": "Large protest mobilization reported in urban centers following political disputes.",
        "metadata": {"impact": "medium", "sentiment": "tense"},
        "occurred_at": datetime.utcnow() - timedelta(hours=2),
    },
    {
        "source": "NewsAPI",
        "topic": "economy",
        "event_type": "policy update",
        "country": "India",
        "region": "Asia",
        "latitude": 28.61,
        "longitude": 77.21,
        "severity": 6,
        "summary": "Government announces infrastructure spending package aimed at reducing logistics bottlenecks.",
        "metadata": {"impact": "medium", "sentiment": "stable"},
        "occurred_at": datetime.utcnow() - timedelta(hours=3),
    },
    {
        "source": "WHO",
        "topic": "health",
        "event_type": "outbreak",
        "country": "Brazil",
        "region": "South America",
        "latitude": -15.78,
        "longitude": -47.93,
        "severity": 8,
        "summary": "Hospital systems report increased demand in high-risk districts amid disease surveillance updates.",
        "metadata": {"impact": "high", "sentiment": "concern"},
        "occurred_at": datetime.utcnow() - timedelta(hours=5),
    },
    {
        "source": "NASA",
        "topic": "climate",
        "event_type": "weather alert",
        "country": "United States",
        "region": "North America",
        "latitude": 34.05,
        "longitude": -118.24,
        "severity": 7,
        "summary": "Extreme heat warnings expand as temperatures climb across multiple west-central regions.",
        "metadata": {"impact": "medium", "sentiment": "alert"},
        "occurred_at": datetime.utcnow() - timedelta(hours=6),
    },
    {
        "source": "UN",
        "topic": "migration",
        "event_type": "border crossing",
        "country": "Tunisia",
        "region": "Africa",
        "latitude": 36.8,
        "longitude": 10.18,
        "severity": 5,
        "summary": "Cross-border movement surges as humanitarian organizations increase support activities.",
        "metadata": {"impact": "medium", "sentiment": "watch"},
        "occurred_at": datetime.utcnow() - timedelta(hours=9),
    },
    {
        "source": "EM-DAT",
        "topic": "disaster",
        "event_type": "flood",
        "country": "Pakistan",
        "region": "Asia",
        "latitude": 33.7,
        "longitude": 73.07,
        "severity": 8,
        "summary": "River levels rise after intense rainfall, forcing emergency response around vulnerable settlements.",
        "metadata": {"impact": "high", "sentiment": "urgent"},
        "occurred_at": datetime.utcnow() - timedelta(hours=10),
    },
    {
        "source": "World Bank",
        "topic": "economy",
        "event_type": "macro indicator",
        "country": "Nigeria",
        "region": "Africa",
        "latitude": 9.08,
        "longitude": 7.4,
        "severity": 5,
        "summary": "Inflation indicators remain elevated while transport and food costs remain under pressure.",
        "metadata": {"impact": "medium", "sentiment": "watch"},
        "occurred_at": datetime.utcnow() - timedelta(hours=12),
    },
]

SEED_STATISTICS = [
    {"metric": "inflation", "country": "Ukraine", "region": "Europe", "value": 11.8, "unit": "%", "source": "World Bank", "metadata": {"trend": "up"}, "as_of_date": datetime.utcnow() - timedelta(days=1)},
    {"metric": "gdp_growth", "country": "India", "region": "Asia", "value": 6.2, "unit": "%", "source": "World Bank", "metadata": {"trend": "stable"}, "as_of_date": datetime.utcnow() - timedelta(days=1)},
    {"metric": "cases", "country": "Brazil", "region": "South America", "value": 4820, "unit": "count", "source": "WHO", "metadata": {"trend": "up"}, "as_of_date": datetime.utcnow() - timedelta(days=1)},
    {"metric": "temperature", "country": "United States", "region": "North America", "value": 39.3, "unit": "C", "source": "NOAA", "metadata": {"trend": "up"}, "as_of_date": datetime.utcnow() - timedelta(days=1)},
    {"metric": "inflation", "country": "Nigeria", "region": "Africa", "value": 24.1, "unit": "%", "source": "IMF", "metadata": {"trend": "up"}, "as_of_date": datetime.utcnow() - timedelta(days=1)},
    {"metric": "displacement", "country": "Tunisia", "region": "Africa", "value": 21000, "unit": "people", "source": "UNHCR", "metadata": {"trend": "up"}, "as_of_date": datetime.utcnow() - timedelta(days=1)},
    {"metric": "rainfall", "country": "Pakistan", "region": "Asia", "value": 148, "unit": "mm", "source": "Meteorological Service", "metadata": {"trend": "up"}, "as_of_date": datetime.utcnow() - timedelta(days=1)},
]


def seed_database() -> None:
    db = SessionLocal()
    try:
        if db.query(EventRecord).count() == 0:
            for item in SEED_EVENTS:
                db.add(EventRecord(**item))
        if db.query(StatisticRecord).count() == 0:
            for item in SEED_STATISTICS:
                db.add(StatisticRecord(**item))
        db.commit()
    finally:
        db.close()


def get_events() -> List[dict]:
    db = SessionLocal()
    try:
        rows = db.query(EventRecord).order_by(EventRecord.occurred_at.desc()).limit(20).all()
        return [
            {
                "id": row.id,
                "source": row.source,
                "topic": row.topic,
                "event_type": row.event_type,
                "country": row.country,
                "region": row.region,
                "latitude": row.latitude,
                "longitude": row.longitude,
                "severity": row.severity,
                "summary": row.summary,
                "metadata": row.metadata,
                "occurred_at": row.occurred_at.isoformat(),
            }
            for row in rows
        ]
    finally:
        db.close()


def get_statistics() -> List[dict]:
    db = SessionLocal()
    try:
        rows = db.query(StatisticRecord).order_by(StatisticRecord.as_of_date.desc()).limit(20).all()
        return [
            {
                "id": row.id,
                "metric": row.metric,
                "country": row.country,
                "region": row.region,
                "value": row.value,
                "unit": row.unit,
                "source": row.source,
                "as_of_date": row.as_of_date.isoformat(),
                "metadata": row.metadata,
            }
            for row in rows
        ]
    finally:
        db.close()


def add_event(event_payload: dict) -> dict:
    db = SessionLocal()
    try:
        record = EventRecord(**event_payload)
        db.add(record)
        db.commit()
        db.refresh(record)
        return {
            "id": record.id,
            "source": record.source,
            "topic": record.topic,
            "event_type": record.event_type,
            "country": record.country,
            "region": record.region,
            "latitude": record.latitude,
            "longitude": record.longitude,
            "severity": record.severity,
            "summary": record.summary,
            "metadata": record.metadata,
            "occurred_at": record.occurred_at.isoformat(),
        }
    finally:
        db.close()


def add_stat(stat_payload: dict) -> dict:
    db = SessionLocal()
    try:
        record = StatisticRecord(**stat_payload)
        db.add(record)
        db.commit()
        db.refresh(record)
        return {
            "id": record.id,
            "metric": record.metric,
            "country": record.country,
            "region": record.region,
            "value": record.value,
            "unit": record.unit,
            "source": record.source,
            "as_of_date": record.as_of_date.isoformat(),
            "metadata": record.metadata,
        }
    finally:
        db.close()
