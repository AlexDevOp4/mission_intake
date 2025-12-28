#!/usr/bin/env bash
set -e

echo "Starting deployment..."

echo "Pulling latest code"
git pull origin main

echo "Building containers"
docker compose build

echo "Restarting services"
docker compose up -d

echo "Deployment finished"
