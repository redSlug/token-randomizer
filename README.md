# Token Randomizer

A web application that selects a ranom token in a user provided image.

## Setup

### Backend

```bash
cd backend
python3.11 -m venv venv
pip install -r requirements.txt
flask --app run.py run --debug
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Features

- Upload images
- Process images and select random token in image
- View original and selected token side by side

## Tech Stack

- Backend: Flask, Python
- Frontend: React, Vite

## Backend local develoment

### Docker

```bash
docker build -t local/token-randomizer .
docker run -p 5009:5000 --name randomizer local/token-randomizer
docker stop randomizer
docker rm randomizer
```

### Docker compose

```bash
docker compose build
docker compose up -d --force-recreate
```
