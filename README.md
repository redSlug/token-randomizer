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
