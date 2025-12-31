#!/usr/bin/env bash
set -e

echo "Starting deployment..."
export AWS_DEFAULT_REGION=us-east-1

get_ssm() {
    local name="$1"

    aws ssm get-parameter \
    --name "$name" \
    --with-decryption \
    --query "Parameter.Value" \
    --output text
}

ALLOWED_HOSTS=$(get_ssm "/mission-intake/prod/ALLOWED_HOSTS")
DJANGO_SECRET_KEY=$(get_ssm "/mission-intake/prod/DJANGO_SECRET_KEY")
POSTGRES_DB=$(get_ssm "/mission-intake/prod/POSTGRES_DB")
POSTGRES_PASSWORD=$(get_ssm "/mission-intake/prod/POSTGRES_PASSWORD")
POSTGRES_PORT=$(get_ssm "/mission-intake/prod/POSTGRES_PORT")
POSTGRES_USER=$(get_ssm "/mission-intake/prod/POSTGRES_USER")
SOLR_URL=$(get_ssm "/mission-intake/prod/SOLR_URL")

export ALLOWED_HOSTS
export DJANGO_SECRET_KEY
export POSTGRES_DB
export POSTGRES_PASSWORD
export POSTGRES_PORT
export POSTGRES_USER
export SOLR_URL

echo "Pulling latest code"
git pull origin main

echo "Building containers"
docker compose build

echo "Restarting services"
docker compose up -d --build

echo "Deployment finished"
