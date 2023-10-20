# Use the official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Install FastAPI and Uvicorn
RUN pip install --upgrade pip \
    && pip install fastapi uvicorn websockets

# Copy the FastAPI application code into the container
COPY . /app

# Expose the port that the FastAPI application will run on
EXPOSE 8000

# Command to run the FastAPI application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
