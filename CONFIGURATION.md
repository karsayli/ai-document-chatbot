# Configuration Instructions

This document describes all configuration files, parameters, and their settings for the Document Chatbot application.

## Configuration File Locations

### Backend Configuration

**File:** `backend/.env`

**Location:** `backend/.env` (create from `backend/.env.example`)

**Example file:** `backend/.env.example`

### Frontend Configuration

Frontend is a static build and doesn't require runtime configuration files. API endpoint is configured in the React source code.

## Backend Configuration Parameters

### Required Parameters

#### `GOOGLE_API_KEY`
- **Description**: Google Gemini API key for chat functionality
- **Type**: String
- **Required**: Yes
- **Default**: None
- **Example**: `GOOGLE_API_KEY=AIzaSyAbCdEf1234567890`
- **How to obtain**: 
  1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
  2. Sign in with your Google account
  3. Create a new API key
  4. Copy the key to your `.env` file
- **Security**: Keep this key secure. Never commit to version control.

### Optional Parameters

#### `OPENAI_API_KEY`
- **Description**: OpenAI API key for enhanced embeddings (optional)
- **Type**: String
- **Required**: No
- **Default**: None (sentence-transformers will be used as fallback)
- **Example**: `OPENAI_API_KEY=sk-abcdefghijklmnopqrstuvwxyz1234567890`
- **How to obtain**: 
  1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
  2. Sign in or create an account
  3. Create a new API key
  4. Copy the key to your `.env` file
- **Note**: If not provided, the system uses sentence-transformers locally (slower but no API costs)

#### `HOST`
- **Description**: Server host address
- **Type**: String
- **Required**: No
- **Default**: `0.0.0.0` (all interfaces)
- **Example**: `HOST=0.0.0.0` or `HOST=127.0.0.1`
- **Note**: Use `0.0.0.0` for Docker containers, `127.0.0.1` for local development only

#### `PORT`
- **Description**: Server port number
- **Type**: Integer
- **Required**: No
- **Default**: `8000`
- **Example**: `PORT=8000`
- **Note**: Ensure the port is not in use by another application

#### `LOG_LEVEL`
- **Description**: Logging verbosity level
- **Type**: String
- **Required**: No
- **Default**: `INFO`
- **Valid values**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- **Example**: `LOG_LEVEL=DEBUG`
- **Note**: Use `DEBUG` for development, `INFO` or higher for production

## Configuration File Example

**Complete `.env` file example:**

```env
# Required: Google Gemini API Key
GOOGLE_API_KEY=AIzaSyAbCdEf1234567890

# Optional: OpenAI API Key (for better embeddings)
OPENAI_API_KEY=sk-abcdefghijklmnopqrstuvwxyz1234567890

# Optional: Server Configuration
HOST=0.0.0.0
PORT=8000

# Optional: Logging
LOG_LEVEL=INFO
```

## Frontend Configuration

### API Endpoint Configuration

The frontend API endpoint is configured in the React source code:

**File:** `frontend/src/App.js`

**Current configuration:**
```javascript
const API_BASE_URL = 'http://127.0.0.1:8000';
```

**To change the API endpoint:**
1. Edit `frontend/src/App.js`
2. Update `API_BASE_URL` constant
3. Rebuild the frontend: `npm run build`

**For production:**
- Use environment variables or build-time configuration
- Update API endpoint to match your backend URL
- Ensure CORS is configured in backend for the frontend domain

## Docker Configuration

### Docker Compose Configuration

**File:** `docker-compose.yml`

**Key parameters:**
- **Ports**: Backend (8000), Frontend (80)
- **Volumes**: `uploads/`, `chroma_db/`
- **Environment**: Loaded from `backend/.env`

**Customization:**
- Change port mappings in `ports` section
- Modify volume paths as needed
- Add additional environment variables

### Dockerfile Configuration

**Backend Dockerfile:** `backend/Dockerfile`
- Base image: `python:3.11-slim`
- Working directory: `/app`
- Exposed port: `8000`

**Frontend Dockerfile:** `frontend/Dockerfile`
- Build stage: `node:18-alpine`
- Production stage: `nginx:alpine`
- Exposed port: `80`

## Environment-Specific Configuration

### Development Environment

```env
GOOGLE_API_KEY=your-dev-key
LOG_LEVEL=DEBUG
HOST=127.0.0.1
PORT=8000
```

### Staging Environment

```env
GOOGLE_API_KEY=your-staging-key
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8000
```

### Production Environment

```env
GOOGLE_API_KEY=your-production-key
OPENAI_API_KEY=your-production-openai-key
LOG_LEVEL=WARNING
HOST=0.0.0.0
PORT=8000
```

## Configuration Validation

### Verify Configuration

**Check backend configuration:**
```bash
# Test if .env file is loaded
cd backend
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('GOOGLE_API_KEY:', 'Set' if os.getenv('GOOGLE_API_KEY') else 'Not set')"
```

**Check Docker environment:**
```bash
docker-compose config
```

## Security Best Practices

1. **Never commit `.env` files** to version control
2. **Use different API keys** for different environments
3. **Rotate API keys** regularly
4. **Use secrets management** in production (Docker secrets, Kubernetes secrets, etc.)
5. **Restrict file permissions**: `chmod 600 backend/.env`

## Troubleshooting Configuration

### Common Issues

**Problem: API key not found**
- **Solution**: Verify `.env` file exists in `backend/` directory
- **Solution**: Check file name is exactly `.env` (not `.env.txt`)
- **Solution**: Ensure no extra spaces in configuration values

**Problem: Port conflicts**
- **Solution**: Change `PORT` in `.env` file
- **Solution**: Update `docker-compose.yml` port mapping
- **Solution**: Stop conflicting services

**Problem: Configuration not loading**
- **Solution**: Verify file location (`backend/.env`)
- **Solution**: Check file format (no spaces around `=`)
- **Solution**: Restart services after configuration changes

## Configuration Reference

For detailed information about:
- Environment setup: See [ENVIRONMENT.md](ENVIRONMENT.md)
- Deployment: See [DEPLOYMENT.md](DEPLOYMENT.md)
- Logging: See [LOGGING.md](LOGGING.md)
- Administration: See [ADMIN_GUIDE.md](ADMIN_GUIDE.md)
