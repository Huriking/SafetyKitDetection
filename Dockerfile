# Base image
FROM ultralytics/ultralytics:latest-cpu

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend /app/backend
COPY frontend /app/frontend


# Set the environment variable to tell the app where to find the credentials

# Expose the port the app will run on
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]

