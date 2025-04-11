# Use a slim Python image
FROM python:3.10-slim

# Environment variables to prevent .pyc files and buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory to /app
WORKDIR /app

# Copy everything in the build context (i.e. the backend folder) to /app
COPY . /app/

# Install dependencies from requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose port 8000 (this is the port your app will run on)
EXPOSE 8000

# Run Gunicorn to serve the application; this assumes your Django project folder is named "core"
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
