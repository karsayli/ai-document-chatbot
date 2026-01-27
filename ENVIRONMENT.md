# Environment and Dependencies

This document describes the system requirements, dependencies, and environment setup for the Document Chatbot application.

## System Requirements

### Operating System

**Supported Operating Systems:**
- Linux (Ubuntu 20.04+, Debian 11+, CentOS 8+, RHEL 8+)
- macOS (10.15+)
- Windows 10/11 (with WSL2 recommended)

### Hardware Requirements

**Minimum:**
- CPU: 2 cores
- RAM: 4 GB
- Storage: 10 GB free space
- Network: Internet connection

**Recommended:**
- CPU: 4+ cores
- RAM: 8 GB or more
- Storage: 20 GB free space
- Network: Stable internet connection (for API calls)

## Software Dependencies

### Required Software

#### Docker (Recommended)
- **Version**: 20.10 or higher
- **Purpose**: Containerized deployment
- **Installation**: [Docker Installation Guide](https://docs.docker.com/get-docker/)

#### Docker Compose (Optional but Recommended)
- **Version**: 1.29 or higher
- **Purpose**: Multi-container orchestration
- **Installation**: Usually included with Docker Desktop

#### Git
- **Version**: 2.0 or higher
- **Purpose**: Version control and repository cloning
- **Installation**: [Git Installation Guide](https://git-scm.com/downloads)

### Development Dependencies (For Manual Installation)

#### Python
- **Version**: 3.11 or higher (3.8+ minimum)
- **Purpose**: Backend runtime
- **Installation**: [Python Installation Guide](https://www.python.org/downloads/)
- **Verification**: `python --version` or `python3 --version`

#### Node.js
- **Version**: 18.0 or higher
- **Purpose**: Frontend build tool
- **Installation**: [Node.js Installation Guide](https://nodejs.org/)
- **Verification**: `node --version`

#### npm
- **Version**: 9.0 or higher (comes with Node.js)
- **Purpose**: Frontend package management
- **Verification**: `npm --version`

## Backend Dependencies

### Python Packages

**Location:** `backend/requirements.txt`

**Core Dependencies:**

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | >=0.104.0 | Web framework for API |
| uvicorn[standard] | >=0.24.0 | ASGI server |
| python-multipart | >=0.0.6 | File upload support |
| pydantic | >=2.5.0 | Data validation |
| chromadb | >=0.4.18 | Vector database for embeddings |
| pymupdf | >=1.23.0 | PDF text extraction |
| python-docx | >=1.1.0 | DOCX text extraction |
| openai | >=1.3.0 | OpenAI API client (optional) |
| sentence-transformers | >=2.2.0 | Local embeddings (fallback) |
| python-dotenv | >=1.0.0 | Environment variable management |
| google-generativeai | >=0.3.0 | Google Gemini API client |
| requests | >=2.31.0 | HTTP client |

**Installation:**
```bash
cd backend
pip install -r requirements.txt
```

**Virtual Environment (Recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Frontend Dependencies

### Node.js Packages

**Location:** `frontend/package.json`

**Core Dependencies:**

| Package | Version | Purpose |
|---------|---------|---------|
| react | ^18.2.0 | UI library |
| react-dom | ^18.2.0 | React DOM rendering |
| react-scripts | 5.0.1 | Build tools and scripts |
| axios | ^1.6.2 | HTTP client for API calls |

**Installation:**
```bash
cd frontend
npm install
```

## Containerized Deployment (Docker)

### Docker Images

**Backend Image:**
- **Base Image**: `python:3.11-slim`
- **Dockerfile**: `backend/Dockerfile`
- **Size**: ~500 MB (with dependencies)

**Frontend Image:**
- **Build Stage**: `node:18-alpine`
- **Production Stage**: `nginx:alpine`
- **Dockerfile**: `frontend/Dockerfile`
- **Size**: ~50 MB (production build)

**Docker Compose:**
- **File**: `docker-compose.yml`
- **Services**: `backend`, `frontend`
- **Network**: `document-chatbot-network`

## External Systems and Services

### Required External Services

#### Google Gemini API
- **Purpose**: AI chat generation
- **Required**: Yes
- **API Key**: Required (see [CONFIGURATION.md](CONFIGURATION.md))
- **Documentation**: [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Rate Limits**: Check Google's documentation
- **Cost**: Free tier available, usage-based pricing

### Optional External Services

#### OpenAI API
- **Purpose**: Enhanced embeddings and chat fallback
- **Required**: No (sentence-transformers used as fallback)
- **API Key**: Optional
- **Documentation**: [OpenAI Platform](https://platform.openai.com/)
- **Rate Limits**: Check OpenAI's documentation
- **Cost**: Pay-per-use pricing

## Local Services

### ChromaDB
- **Purpose**: Vector database for document embeddings
- **Type**: Local (embedded)
- **Location**: `backend/chroma_db/` directory
- **Storage**: Persistent on disk
- **Setup**: Automatic (no manual configuration needed)
- **Data**: Stored locally, not in cloud

## Environment Setup

### Quick Start with Docker (Recommended)

1. **Install Docker and Docker Compose**
2. **Clone repository:**
   ```bash
   git clone https://gitlab.fit.cvut.cz/karsayli/sp2.git
   cd sp2
   ```
3. **Configure environment:**
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env and add API keys
   ```
4. **Start services:**
   ```bash
   docker-compose up -d
   ```

### Manual Setup (Without Docker)

1. **Install Python 3.11+ and Node.js 18+**
2. **Setup backend:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Setup frontend:**
   ```bash
   cd frontend
   npm install
   ```
4. **Configure environment:**
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env
   ```
5. **Start services:**
   ```bash
   # Terminal 1: Backend
   cd backend
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
   
   # Terminal 2: Frontend
   cd frontend
   npm start
   ```

## Development Environment

### Recommended Tools

- **IDE**: VS Code, PyCharm, or any Python/JavaScript IDE
- **Version Control**: Git
- **API Testing**: Postman, curl, or browser
- **Container Management**: Docker Desktop

### Development Setup

1. **Clone repository**
2. **Install dependencies** (see above)
3. **Configure `.env` file**
4. **Run in development mode:**
   - Backend: `uvicorn app.main:app --reload`
   - Frontend: `npm start`

## Production Environment

### Recommended Production Setup

- **Container Orchestration**: Docker Compose, Kubernetes, or similar
- **Reverse Proxy**: Nginx or Apache (for SSL/TLS)
- **Process Manager**: systemd, supervisor, or Docker
- **Monitoring**: Application logs, health checks
- **Backup**: Automated backups of ChromaDB and uploads

### Production Considerations

- Use environment variables for sensitive data
- Enable HTTPS/SSL
- Set up proper logging and monitoring
- Configure firewall rules
- Implement backup procedures
- Use secrets management for API keys

## Dependency Updates

### Updating Backend Dependencies

```bash
cd backend
pip install --upgrade -r requirements.txt
```

### Updating Frontend Dependencies

```bash
cd frontend
npm update
```

### Security Updates

- Regularly update dependencies for security patches
- Use `npm audit` for frontend
- Use `pip-audit` or `safety` for backend
- CI/CD pipeline includes automated security scanning

## Troubleshooting

### Dependency Installation Issues

**Python packages:**
- Ensure Python 3.11+ is installed
- Use virtual environment
- Check internet connection
- Try: `pip install --upgrade pip`

**Node.js packages:**
- Ensure Node.js 18+ is installed
- Clear npm cache: `npm cache clean --force`
- Delete `node_modules` and `package-lock.json`, then reinstall

**Docker issues:**
- Ensure Docker is running
- Check Docker version compatibility
- Verify disk space available

## Additional Resources

- [Python Documentation](https://docs.python.org/3/)
- [Node.js Documentation](https://nodejs.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)

For more information:
- [ADMIN_GUIDE.md](ADMIN_GUIDE.md) - Administration guide
- [CONFIGURATION.md](CONFIGURATION.md) - Configuration details
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment instructions
