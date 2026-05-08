# Use official Python image
FROM python:3.11.9-slim-bookworm

# Set working directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

#UPGRADE PIP/SETUPTOOLS/WHEEL
RUN pip install --upgrade pip setuptools wheel

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose Flask port
EXPOSE 5000

# Environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run application
CMD ["flask", "run"]
