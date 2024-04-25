# Install base Python image
FROM python:3.11-slim-bullseye

WORKDIR /usr/local/app

# Python won't create .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# Disable python stdout
ENV PYTHONUNBUFFERED 1

# Redis host config
ENV REDIS_HOST redis
ENV REDIS_PORT 6379

# Flask host config
ENV FLASK_HOST 0.0.0.0
ENV FLASK_PORT 80

# Copy files to the container
COPY . .

# Install dependencies
RUN  pip3 install --no-cache-dir --upgrade pip \
   && pip3 install --no-cache-dir -r requirements.txt

# Flask entrypoint
ENTRYPOINT ["/usr/local/bin/python", "flask_redis_editor.py"]

