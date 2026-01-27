#!/bin/bash

# Deployment script for Document Chatbot
# This script can be used for manual deployment or integrated into CI/CD

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
ENVIRONMENT=${1:-staging}
BACKEND_IMAGE=${BACKEND_IMAGE:-"gitlab.fit.cvut.cz:5050/karsayli/sp2/backend:main"}
FRONTEND_IMAGE=${FRONTEND_IMAGE:-"gitlab.fit.cvut.cz:5050/karsayli/sp2/frontend:main"}

echo -e "${GREEN}=========================================="
echo "Document Chatbot Deployment"
echo "==========================================${NC}"
echo "Environment: $ENVIRONMENT"
echo "Backend Image: $BACKEND_IMAGE"
echo "Frontend Image: $FRONTEND_IMAGE"
echo ""

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed or not in PATH${NC}"
    exit 1
fi

# Pull images
echo -e "${YELLOW}Pulling Docker images...${NC}"
docker pull $BACKEND_IMAGE || echo "Warning: Could not pull backend image"
docker pull $FRONTEND_IMAGE || echo "Warning: Could not pull frontend image"

# Deploy using docker-compose
if [ -f "docker-compose.yml" ]; then
    echo -e "${YELLOW}Deploying with docker-compose...${NC}"
    docker-compose pull
    docker-compose up -d --no-deps
    
    echo -e "${GREEN}Waiting for services to be healthy...${NC}"
    sleep 5
    
    # Health check
    if curl -f http://localhost:8000/api/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Backend health check passed${NC}"
    else
        echo -e "${RED}❌ Backend health check failed${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
    echo ""
    echo "Services are running at:"
    echo "  - Backend: http://localhost:8000"
    echo "  - Frontend: http://localhost"
else
    echo -e "${YELLOW}docker-compose.yml not found. Skipping docker-compose deployment.${NC}"
    echo "You can deploy manually using the images:"
    echo "  - $BACKEND_IMAGE"
    echo "  - $FRONTEND_IMAGE"
fi
