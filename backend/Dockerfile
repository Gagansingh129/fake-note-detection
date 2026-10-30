# NoteGuard AI - Backend Container with Preinstalled TensorFlow & CUDA/CPU Runtime
FROM tensorflow/tensorflow:latest

# Prevent Python from writing .pyc files & buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TF_ENABLE_ONEDNN_OPTS=0 \
    MPLCONFIGDIR=/tmp/matplotlib

WORKDIR /app

# Install lightweight backend dependencies (OpenCV, FastAPI, Uvicorn, SQLAlchemy)
COPY requirements.docker.txt /app/requirements.txt
RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r requirements.txt

# Copy backend application source code
COPY app /app/app
COPY run_server.py /app/run_server.py

# Copy pre-trained model artifacts and registry
COPY models /app/models

# Create required runtime directories
RUN mkdir -p /app/data /app/uploads /app/results/gradcam /tmp/matplotlib

# Expose FastAPI service port
EXPOSE 8000

# Container Healthcheck using Python standard library
HEALTHCHECK --interval=20s --timeout=10s --start-period=30s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health', timeout=5)" || exit 1

# Start Uvicorn ASGI server binding to 0.0.0.0 for external container access
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
