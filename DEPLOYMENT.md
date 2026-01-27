# Deployment Guide

This document describes how to deploy the Document Chatbot application using Docker and CI/CD pipelines.

## Prerequisites

- Docker and Docker Compose installed
- GitLab CI/CD runner configured (for automated deployment)
- Access to GitLab Container Registry (if using CI/CD)

## Deployment Methods

### Method 1: Docker Compose (Recommended for Development/Staging)

1. **Clone the repository:**
   ```bash
   git clone https://gitlab.fit.cvut.cz/karsayli/sp2.git
   cd sp2
   ```

2. **Create environment file:**
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env and add your API keys
   ```

3. **Start services:**
   ```bash
   docker-compose up -d
   ```

4. **Verify deployment:**
   - Backend API: http://localhost:8000
   - Frontend: http://localhost
   - Health check: http://localhost:8000/api/health

5. **View logs:**
   ```bash
   docker-compose logs -f
   ```

6. **Stop services:**
   ```bash
   docker-compose down
   ```

### Method 2: Individual Docker Containers

#### Backend

1. **Build the image:**
   ```bash
   cd backend
   docker build -t document-chatbot-backend:latest .
   ```

2. **Run the container:**
   ```bash
   docker run -d \
     --name chatbot-backend \
     -p 8000:8000 \
     -e GOOGLE_API_KEY=your_key_here \
     -e OPENAI_API_KEY=your_key_here \
     -v $(pwd)/uploads:/app/uploads \
     -v $(pwd)/chroma_db:/app/chroma_db \
     document-chatbot-backend:latest
   ```

#### Frontend

1. **Build the image:**
   ```bash
   cd frontend
   docker build -t document-chatbot-frontend:latest .
   ```

2. **Run the container:**
   ```bash
   docker run -d \
     --name chatbot-frontend \
     -p 80:80 \
     document-chatbot-frontend:latest
   ```

### Method 3: CI/CD Automated Deployment

The project includes a GitLab CI/CD pipeline (`.gitlab-ci.yml`) that automates:

1. **Build stages:**
   - Builds Docker images for backend and frontend
   - Pushes images to GitLab Container Registry

2. **Test stages:**
   - Runs backend tests (if available)
   - Runs frontend tests and builds
   - Performs security scanning

3. **Deploy stages:**
   - Manual deployment to staging (from `develop` branch)
   - Manual deployment to production (from `main` branch or tags)
   - Deploy stages show detailed deployment information and example commands
   - Customize deployment commands based on your infrastructure (Docker, Kubernetes, etc.)

#### Setting up CI/CD

1. **Configure GitLab CI/CD variables:**
   - Go to Project Settings → CI/CD → Variables
   - Add required variables:
     - `CI_REGISTRY_USER`: GitLab registry username
     - `CI_REGISTRY_PASSWORD`: GitLab registry password
     - `GOOGLE_API_KEY`: Google API key (masked, protected)
     - `OPENAI_API_KEY`: OpenAI API key (optional, masked, protected)

2. **Configure GitLab Runner:**
   - Ensure Docker-in-Docker (DinD) is available
   - Configure runner with appropriate tags

3. **Trigger pipeline:**
   - Push to `main` or `develop` branch
   - Create a tag for production release
   - Pipeline will run automatically

#### Deployment Process

**Staging Deployment:**
- Triggered manually from `develop` branch
- Go to CI/CD → Pipelines → Click on pipeline → Click "deploy_staging" → Click "Play" button
- Review deployment information and image tags
- Customize deployment commands for your infrastructure

**Production Deployment:**
- Triggered manually from `main` branch or tags
- Go to CI/CD → Pipelines → Click on pipeline → Click "deploy_production" → Click "Play" button
- ⚠️ **Warning**: Production deployment requires careful verification
- Review deployment information and image tags
- Customize deployment commands for your infrastructure

**Deployment Commands Examples:**

The deploy stages provide example commands that you can customize:

**Docker Compose:**
```bash
docker pull $BACKEND_IMAGE
docker pull $FRONTEND_IMAGE
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d --no-deps
```

**Kubernetes:**
```bash
kubectl set image deployment/backend backend=$BACKEND_IMAGE -n production
kubectl set image deployment/frontend frontend=$FRONTEND_IMAGE -n production
kubectl rollout status deployment/backend -n production
```

**SSH Deployment:**
```bash
ssh user@server "docker pull $BACKEND_IMAGE && docker-compose up -d"
```

## Environment Variables

### Backend

Required environment variables:

- `GOOGLE_API_KEY`: Google Gemini API key (required)
- `OPENAI_API_KEY`: OpenAI API key (optional, for embeddings)

These can be set via:
- `.env` file in `backend/` directory
- Docker environment variables
- CI/CD pipeline variables

### Frontend

Frontend is a static build and doesn't require environment variables at runtime. API endpoint is configured in the React application.

## Health Checks

Both services include health checks:

- **Backend:** `GET /api/health`
- **Frontend:** HTTP check on root path

## Monitoring

### View Container Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Container Status

```bash
docker-compose ps
```

## Troubleshooting

### Backend Issues

1. **API key errors:**
   - Verify `.env` file exists and contains valid keys
   - Check environment variables in Docker container

2. **Port conflicts:**
   - Change port mapping in `docker-compose.yml`
   - Ensure port 8000 is not in use

3. **Permission errors:**
   - Check volume permissions for `uploads/` and `chroma_db/` directories

### Frontend Issues

1. **Cannot connect to backend:**
   - Verify backend is running
   - Check CORS settings in backend
   - Update API endpoint in frontend configuration

2. **Build failures:**
   - Check Node.js version (requires 18+)
   - Clear npm cache: `npm cache clean --force`

### CI/CD Issues

1. **Pipeline failures:**
   - Check GitLab Runner logs
   - Verify Docker-in-Docker is configured
   - Check Container Registry permissions

2. **Security scan failures:**
   - Review security scan reports
   - Update vulnerable dependencies
   - Security stage is set to `allow_failure: true` by default

## Rollback Procedure

### Docker Compose

```bash
# Stop current version
docker-compose down

# Checkout previous version
git checkout <previous-tag>

# Start previous version
docker-compose up -d
```

### CI/CD Rollback

1. Go to GitLab → Deployments
2. Select the previous successful deployment
3. Click "Rollback" button

## Production Considerations

1. **Use environment-specific configuration files**
2. **Set up proper logging and monitoring**
3. **Configure backup procedures for ChromaDB data**
4. **Use secrets management for API keys**
5. **Set up SSL/TLS certificates**
6. **Configure firewall rules**
7. **Set up automated backups**

## Support

For deployment issues, check:
- Application logs
- GitLab CI/CD pipeline logs
- Container logs
- Health check endpoints
