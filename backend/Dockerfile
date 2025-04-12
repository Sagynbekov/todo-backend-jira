# Use a slim Python image
FROM python:3.10-slim

# Environment variables to prevent .pyc files and buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container to /app
WORKDIR /app

# 1️⃣ Copy the requirements file (it's already in the current directory)
COPY requirements.txt /app/

# 2️⃣ Install dependencies using the requirements file
RUN pip install --upgrade pip && pip install -r requirements.txt

# 3️⃣ Copy the rest of the backend code into the container
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Run Gunicorn to serve the Django application
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
