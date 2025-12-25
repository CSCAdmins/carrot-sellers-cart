#!/bin/bash
# Start Carrot Sellers site with Docker

set -e

IMAGE_NAME="carrot-sellers"
CONTAINER_NAME="carrot-sellers-web"
PORT=8080

echo "🥕 Starting Carrot Sellers site with Docker..."
echo ""

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop and try again."
    exit 1
fi

# Build the Docker image
echo "Building Docker image..."
docker build --tag ${IMAGE_NAME} --file Dockerfile .

# Stop and remove existing container if it exists
if docker ps -a | grep -q ${CONTAINER_NAME}; then
    echo "Stopping existing container..."
    docker stop ${CONTAINER_NAME} 2>/dev/null || true
    docker rm ${CONTAINER_NAME} 2>/dev/null || true
fi

# Run the container with port mapping
echo "Starting container..."
docker run \
    --name ${CONTAINER_NAME} \
    --detach \
    --publish ${PORT}:8080 \
    --rm \
    ${IMAGE_NAME}

echo ""
echo "✅ Carrot Sellers site is running!"
echo ""
echo "Access the site at:"
echo "  - http://localhost:${PORT}"
echo ""
echo "To view logs:"
echo "  docker logs -f ${CONTAINER_NAME}"
echo ""
echo "To stop the container:"
echo "  docker stop ${CONTAINER_NAME}"
echo ""