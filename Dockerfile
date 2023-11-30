# Use a full Python image for the build stage
FROM python:3.8.13 as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies for building psycopg2
RUN apt-get update \
    && apt-get install -y libpq-dev gcc

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to /app
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Use a slim Python image for the final stage
FROM python:3.8.13-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install libpq5, which provides libpq.so.5
RUN apt-get update \
    && apt-get install -y libpq5

# Copy the installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY . /app/

# Debugging purposes
RUN ls -al /app

# Expose the port on which the application will run
EXPOSE 8000
