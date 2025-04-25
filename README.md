# Demo of coolify backup api endpoints

This is a demo of the coolify backup api endpoints, using Python. 

This was a feature request for [coolify](https://github.com/coollabsio/coolify/issues/5672)

## Setup

1. Clone the repository
2. copy .env.example to .env and set the env variables
3. Make sure you have `uv` installed
4. Run `uv sync` to install the dependencies
5. Run `uv run main.py` to see the demo

## API Endpoints

`GET /api/v1/databases`

`GET /api/v1/databases/{uuid}/backups`

`PATCH /api/v1/databases/{uuid}`

`DELETE /api/v1/databases/{uuid}/backups/{backup_id}`

