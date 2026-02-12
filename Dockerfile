# -------- CPU Optimized Base Image --------
FROM python:3.10-slim

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Working directory
WORKDIR /app

# Install system dependencies (minimal)
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# VERY IMPORTANT: Install CPU-only Torch BEFORE requirements
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

# Copy requirements first (better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose ports
EXPOSE 8000 8501

# Start services
CMD ["bash", "-c", "\
uvicorn backend.main:app --host 0.0.0.0 --port 8000 & \
exec streamlit run ui/streamlit.py --server.port 8501 --server.address 0.0.0.0 \
"]
