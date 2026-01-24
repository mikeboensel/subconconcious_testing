#!/bin/bash

# Run the calculator FastAPI server
uv run uvicorn server:app --reload --host 0.0.0.0 --port 8000
