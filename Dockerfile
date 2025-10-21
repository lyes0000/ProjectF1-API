FROM python:3.11-alpine3.22
LABEL maintainer="lyes"

# Unbuffered logs
ENV PYTHONUNBUFFERED=1

# Optional dev flag
ARG DEV=false

# Install system dependencies
RUN apk add --update --no-cache \
        postgresql-client \
        build-base \
        postgresql-dev \
        musl-dev \
    && rm -rf /var/cache/apk/*

# Create virtualenv
RUN python3 -m venv /py
ENV PATH="/py/bin:$PATH"

# Copy requirements first for caching
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements-dev.txt /tmp/requirements-dev.txt

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then pip install --no-cache-dir -r /tmp/requirements-dev.txt; fi && \
    rm -rf /tmp

# Copy project code
WORKDIR /app
COPY ./app ./
EXPOSE 8000

# Create non-root user
RUN adduser --disabled-password --no-create-home django-user

# Create directories outside /app (no permission issues)
RUN mkdir -p /tmp/f1_cache /tmp/matplotlib && \
    chown -R django-user:django-user /tmp/f1_cache /tmp/matplotlib

# Switch to non-root user
USER django-user

# Default command for dev
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
