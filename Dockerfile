# IT WORKS IN RENDER WHEN THE DOCKER IN THE ROOT DIRECTORY -------------------------------------

# backend/Dockerfile
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 1️⃣ copy only requirements.txt first
COPY backend/requirements.txt /app/

# 2️⃣ install deps
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# 3️⃣ copy the rest of the backend code
COPY backend/ /app/

EXPOSE 8000
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
