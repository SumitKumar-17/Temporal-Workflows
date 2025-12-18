# Temporal Deletion Demo

## Setup
1. Run `docker-compose up --build`
2. Open `frontend/index.html` in your browser to request deletion.
3. Open `frontend/admin.html` in your browser to approve deletion.
4. View Temporal UI at `http://localhost:8080`.

## Architecture
- **Backend**: FastAPI (Port 8000)
- **Worker**: Temporal Worker (Python)
- **Temporal**: Server & UI
- **Redis**: Queue for requests
