#!/usr/bin/env bash
set -euo pipefail

echo "Starting deployment..."

export AWS_DEFAULT_REGION="us-east-1"

get_param () {
  aws ssm get-parameter \
    --name "$1" \
    --with-decryption \
    --query "Parameter.Value" \
    --output text
}

export ALLOWED_HOSTS="$(get_param /mission-intake/prod/ALLOWED_HOSTS)"
export DJANGO_SECRET_KEY="$(get_param /mission-intake/prod/DJANGO_SECRET_KEY)"
export POSTGRES_DB="$(get_param /mission-intake/prod/POSTGRES_DB)"
export POSTGRES_PASSWORD="$(get_param /mission-intake/prod/POSTGRES_PASSWORD)"
export POSTGRES_PORT="$(get_param /mission-intake/prod/POSTGRES_PORT)"
export POSTGRES_USER="$(get_param /mission-intake/prod/POSTGRES_USER)"
export SOLR_URL="$(get_param /mission-intake/prod/SOLR_URL)"

echo "Environment variables loaded:"
for var in ALLOWED_HOSTS DJANGO_SECRET_KEY POSTGRES_DB POSTGRES_PASSWORD POSTGRES_PORT POSTGRES_USER SOLR_URL; do
  if [[ -z "${!var}" ]]; then
    echo "❌ $var is NOT set"
    exit 1
  else
    echo "✅ $var is set"
  fi
done

echo "Pulling latest code"
git pull origin main

echo "Building and starting containers"
docker compose up -d --build

echo "Deployment finished successfully"
