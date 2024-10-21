# Stage 1: Build stage
FROM python:3.9-slim as builder

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libssl-dev \
    libsasl2-dev \
    libldap2-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies in a temporary location
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

# Stage 2: Runtime stage
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the necessary files from the build stage (dependencies)
COPY --from=builder /install /usr/local

# Copy the rest of the application files
COPY . /app

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose port 5000 to the outside world
EXPOSE 5000

# Command to run the Flask application
#CMD ["flask", "run", "--host=0.0.0.0"]
CMD ["python", "app.py"]

