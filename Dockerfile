# Base image with CUDA support
FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

# Environment settings
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    build-essential \
    cmake \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN python3 -m pip install --upgrade pip

# Copy requirements first (cache-friendly)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose ports
EXPOSE 8000 8501

# Use exec form + proper signal handling
CMD ["bash", "-c", "\
uvicorn backend.main:app --host 0.0.0.0 --port 8000 & \
exec streamlit run ui/streamlit.py --server.port 8501 --server.address 0.0.0.0 \
"]