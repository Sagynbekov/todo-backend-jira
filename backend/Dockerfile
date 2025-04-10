# Use a slim Python image
FROM python:3.10-slim

# Environment variables to prevent .pyc files and output buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory in container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire backend code into the container
COPY . /app/

# Expose the port Django will run on
EXPOSE 8000

# Use Gunicorn as the production server
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
