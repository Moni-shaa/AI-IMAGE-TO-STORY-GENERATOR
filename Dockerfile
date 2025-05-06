FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip

# Install torch from local wheel
RUN pip install --no-cache-dir ./torch-2.7.0-cp311-cp311-manylinux_2_28_x86_64.whl

# Install other packages
RUN pip install --no-cache-dir --default-timeout=100 --retries=5 -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
