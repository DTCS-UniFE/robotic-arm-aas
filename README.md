# Robotic Arm AAS

A minimal FastAPI-based Asset Administration Shell (AAS) for a simulated robotic arm, with persistent state storage using Redis/Valkey. The API allows querying static and dynamic information about the robotic arm and sending movement commands.

## Features

- **REST API** for robotic arm asset administration
- **Persistent state** using Redis/Valkey
- **Dockerized** for easy deployment
- **GitHub Actions** workflow for building and publishing Docker images

## API Endpoints

| Method | Endpoint         | Description                            |
|--------|------------------|----------------------------------------|
| GET    | `/aas/static`    | Get static info about the robotic arm  |
| GET    | `/aas/state`     | Get current dynamic state              |
| POST   | `/aas/move`      | Move the robot arm to a new position   |

### Example: Move Command

```json
POST /aas/move
{
  "x": 10.0,
  "y": 5.0,
  "z": 2.0
}
```
With:
- `0.0 <= x <= 100.0`
- `-50.0 <= y <= 50.0`
- `0.0 <= z <= 100.0`

## Environment Variables

- `VALKEY_HOST` (default: `localhost`)
- `VALKEY_PORT` (default: `6379`)

## Docker

### With docker compose

Run:
```bash
docker compose up
```

### Manual build and run

Build and run the container:
```bash
docker build -t robotic-arm-aas .

docker run \
    -e VALKEY_HOST=<valkey_or_redis_host> \
    -e VALKEY_PORT=<valkey_or_redis_port> \
    -p 8000:8000 \
    robotic-arm-aas
```

## GitHub Actions

A workflow is provided in [.github/workflows/docker-ghcr.yaml](.github/workflows/docker-ghcr.yaml) to automatically build and push multi-arch Docker images to GitHub Container Registry on push to branches `main` or `master`.

The image will be available at `ghcr.io/repo-owner-name/robotic-arm-aas`, all in lowercase (GHCR does not allow uppercase characters).

For this particular repository, the built Docker image can be found at [ghcr.io/dtcs-unife/robotic-arm-aas](https://ghcr.io/dtcs-unife/robotic-arm-aas).
