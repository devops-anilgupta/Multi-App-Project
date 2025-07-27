# Use an official Python base image
FROM python:3.11-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements file first (for layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose Flask default port
EXPOSE 5000

# Set environment variable to tell Flask to run
ENV FLASK_APP=upload_api.py

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
