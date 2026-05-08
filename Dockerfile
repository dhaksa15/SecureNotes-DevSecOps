# Use official Python image
FROM python:3.11.9-slim-bookworm

# Set working directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade \
	pip==25.0 \
	setuptools==80.0.0 \
	wheel==0.46.1 && \
	pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose Flask port
EXPOSE 5000

# Environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run application
CMD ["flask", "run"]
