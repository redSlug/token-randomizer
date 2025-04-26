FROM python:3.11-slim

WORKDIR /token-randomizer/backend

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 curl -y

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "server.py"]
