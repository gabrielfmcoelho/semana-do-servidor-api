# Use the official Python image as the base
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file (if you have dependencies)
COPY requirements.txt .

# Install any dependencies required
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app to the working directory
COPY . /app

# Set build argument for port
ARG PORT

# Expose the port
EXPOSE ${PORT}

# Command to run the application
CMD ["sh", "-c", "uvicorn app.app:app --host 0.0.0.0 --port ${PORT}"]