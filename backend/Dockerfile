FROM python:3.11

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libpoppler-cpp-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install pip & tooling
RUN pip install --upgrade pip wheel setuptools

# ✅ Copy and install only requirements first to leverage caching
COPY requirements.txt .
RUN pip install --default-timeout=100 --no-cache-dir -r requirements.txt


# ✅ Now copy source code (changing it won't affect requirements install)
COPY app/ ./app

# ✅ Copy .env LAST (changing this won’t bust other layers)
COPY .env .env

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
