from __future__ import annotations

import asyncio
from datetime import datetime
from random import choice, randint, uniform

from app.db import add_event, add_stat, get_events, get_statistics, seed_database

TOPICS = ["conflict", "economy", "health", "climate", "migration", "disaster", "protest"]
COUNTRIES = [
    ("Ukraine", "Europe", 49.0, 32.0),
    ("Kenya", "Africa", -1.29, 36.82),
    ("India", "Asia", 28.61, 77.21),
    ("Brazil", "South America", -15.78, -47.93),
    ("United States", "North America", 34.05, -118.24),
    ("Tunisia", "Africa", 36.8, 10.18),
    ("Pakistan", "Asia", 33.7, 73.07),
    ("Nigeria", "Africa", 9.08, 7.4),
    ("France", "Europe", 48.85, 2.35),
    ("Japan", "Asia", 35.68, 139.69),
]

METRICS = [
    ("inflation", "%"),
    ("gdp_growth", "%"),
    ("cases", "count"),
    ("temperature", "C"),
    ("rainfall", "mm"),
    ("displacement", "people"),
]


def build_live_event() -> dict:
    country, region, lat, lon = choice(COUNTRIES)
    topic = choice(TOPICS)
    event_type = choice(["policy update", "security alert", "weather alert", "civil unrest", "outbreak", "migration surge", "power disruption"])
    summary_templates = {
        "conflict": [
            "Security forces report heightened alert status after new incidents near strategic transport hubs.",
            "Authorities increase mobilization as local conflict dynamics intensify across multiple districts.",
        ],
        "economy": [
            "Market sentiment shifts after new policy signals create uncertainty for supply chains.",
            "Analysts monitor trade data as currency volatility changes expectations for regional growth.",
        ],
        "health": [
            "Rapid testing and response efforts intensify as public health agencies monitor rising demand.",
            "Medical teams report constrained capacity amid a new wave of regional alerts.",
        ],
        "climate": [
            "Meteorological services issue updated warnings as temperatures and rainfall patterns shift.",
            "Extreme weather alerts intensify as climate risk escalates in exposed communities.",
        ],
        "migration": [
            "New displacement patterns emerge as cross-border routes and shelter capacity come under strain.",
            "Aid agencies prepare for fresh movements as local conditions change rapidly.",
        ],
        "disaster": [
            "Emergency response teams expand after the latest impact reports from affected communities.",
            "Critical infrastructure remains under strain as local authorities respond to new hazard warnings.",
        ],
        "protest": [
            "Regional demonstrations and civil mobilization continue as public pressure increases.",
            "New protest activity spreads across urban centers amid sustained calls for reform.",
        ],
    }
    summary = choice(summary_templates.get(topic, ["New information emerges affecting regional stability and response capacity."]))
    return {
        "source": "Live Stream",
        "topic": topic,
        "event_type": event_type,
        "country": country,
        "region": region,
        "latitude": round(lat + uniform(-1.5, 1.5), 4),
        "longitude": round(lon + uniform(-1.5, 1.5), 4),
        "severity": randint(3, 10),
        "summary": summary,
        "metadata": {"impact": choice(["low", "medium", "high"]), "sentiment": choice(["stable", "watch", "volatile"])},
        "occurred_at": datetime.utcnow(),
    }


def build_live_stat() -> dict:
    country, region, _, _ = choice(COUNTRIES)
    metric, unit = choice(METRICS)
    latest_value = round(uniform(1.5, 60.0), 2)
    if metric in ["cases", "displacement"]:
        latest_value = round(uniform(1500, 60000), 0)
    return {
        "metric": metric,
        "country": country,
        "region": region,
        "value": latest_value,
        "unit": unit,
        "source": "Live Feed",
        "metadata": {"trend": choice(["up", "down", "stable"])},
        "as_of_date": datetime.utcnow(),
    }


async def live_stream_loop() -> None:
    seed_database()
    while True:
        add_event(build_live_event())
        add_stat(build_live_stat())
        await asyncio.sleep(12)


def get_summary() -> dict:
    events = get_events()
    stats = get_statistics()
    total_alerts = len(events)
    harshest = max(events, key=lambda item: item["severity"], default={"severity": 0})
    latest_topics = {}
    for event in events:
        latest_topics[event["topic"]] = latest_topics.get(event["topic"], 0) + 1

    return {
        "total_alerts": total_alerts,
        "top_topic": max(latest_topics.items(), key=lambda item: item[1], default=("conflict", 0))[0],
        "max_severity": harshest.get("severity", 0),
        "countries": len({item["country"] for item in events}),
        "latest_statistics": stats[:5],
    }
