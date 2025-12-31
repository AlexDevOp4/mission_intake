FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -r appuser

WORKDIR /app

# Install Python dependencies first (better caching)
COPY backend/requirements.txt backend/requirements.txt
RUN python -m pip install --no-cache-dir -r backend/requirements.txt

# Copy application code
COPY . .

# Fix ownership after copy (important)
RUN chown -R appuser:appuser /app

# Make entrypoint executable
RUN chmod +x /app/entrypoint.prod.sh

# Create the staticfiles directory, and change ownership to appuser.
RUN mkdir -p /app/backend/mission_intake/staticfiles \
    && chown -R appuser:appuser /app/backend/mission_intake/staticfiles
# Switch to non-root user
USER appuser

CMD ["/app/entrypoint.prod.sh"]