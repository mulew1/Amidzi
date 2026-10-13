# README.md
# Amidzi

Amidzi is a live world-events and statistics dashboard built as a full-stack MVP using:

- FastAPI backend
- SQLite persistence for event and statistic records
- Next.js frontend with a live map and KPI cards
- WebSocket streaming for real-time updates
- Docker Compose for local development

## Features

- Live world event feed with country/region filters
- Real-time statistics panel for key metrics
- KPI summary cards across the latest event snapshot
- Map view with event markers using Leaflet
- Timeline with severity and topic filters
- Background data generator to simulate live updates

## Tech stack

- Backend: FastAPI, SQLAlchemy, Pydantic
- Frontend: Next.js, React, Leaflet, Recharts
- Local runtime: Docker Compose

## Run locally

```bash
docker compose up --build
```

Then open:

- Frontend: http://localhost:3000
- API: http://localhost:8000/docs

## Environment variables

The app is configured to run locally without API keys. For production use, set the following environment variables:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BACKEND_CORS_ORIGINS=http://localhost:3000
```

## Project structure

```text
.
├── backend
│   ├── app
│   ├── Dockerfile
│   └── requirements.txt
├── frontend
│   ├── app
│   ├── components
│   ├── Dockerfile
│   ├── next.config.js
│   ├── package.json
│   └── tsconfig.json
├── docker-compose.yml
├── README.md
└── .gitignore
```

## Notes

This is a demo MVP intended to show how a live world view dashboard can be structured and deployed.
The backend includes a background live-update loop that inserts trending events and metric changes into the store so the UI updates over time.
