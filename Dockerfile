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
ENV PORT=${PORT}
ARG HOST
ENV HOST=${HOST}
ARG APP_PORT
ENV APP_PORT=${APP_PORT}
ARG MODE
ENV MODE=${MODE}
ARG PROJECT_NAME
ENV PROJECT_NAME=${PROJECT_NAME}
ARG SECURITY_TOKEN
ARG DB_DRIVER
ENV DB_DRIVER=${DB_DRIVER}
ARG DB_USER
ENV DB_USER=${DB_USER}
ARG DB_PASSWORD
ENV DB_PASSWORD=${DB_PASSWORD}
ARG DB_HOST
ENV DB_HOST=${DB_HOST}
ARG DB_PORT
ENV DB_PORT=${DB_PORT}
ARG DB_NAME
ENV DB_NAME=${DB_NAME}

# Expose the port
EXPOSE ${PORT}

# Command to run the application
CMD ["sh", "-c", "uvicorn api-intermediária:app --host 0.0.0.0 --port ${PORT}"]