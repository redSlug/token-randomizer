# Build stage
FROM --platform=linux/amd64 python:3.11-slim AS builder
WORKDIR /token-randomizer/backend
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 curl -y
COPY requirements.txt .
RUN pip install -r requirements.txt

# Final stage
FROM node:16-alpine
WORKDIR /token-randomizer/backend
COPY --from=builder . .
CMD ["gunicorn", "--bind", "0.0.0.0:3000", "--timeout", "120", "-w", "2", "server:app"]
