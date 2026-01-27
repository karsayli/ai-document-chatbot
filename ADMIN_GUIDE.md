# Administrator Guide

This guide provides comprehensive instructions for system administrators to install, configure, and maintain the Document Chatbot application.

## System Requirements

### Hardware Requirements

**Minimum:**
- CPU: 2 cores
- RAM: 4 GB
- Storage: 10 GB free space
- Network: Internet connection for API access

**Recommended:**
- CPU: 4+ cores
- RAM: 8 GB or more
- Storage: 20 GB free space (for document storage and ChromaDB)
- Network: Stable internet connection

### Software Requirements

- **Operating System**: Linux (Ubuntu 20.04+, Debian 11+, CentOS 8+), macOS, or Windows 10+
- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 1.29 or higher (optional, for easier deployment)
- **Git**: For cloning the repository

## Installation

### Method 1: Docker Compose (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://gitlab.fit.cvut.cz/karsayli/sp2.git
   cd sp2
   ```

2. **Create environment file:**
   ```bash
   cp backend/.env.example backend/.env
   ```

3. **Configure API keys:**
   Edit `backend/.env` and add your API keys:
   ```bash
   GOOGLE_API_KEY=your-google-api-key-here
   OPENAI_API_KEY=your-openai-api-key-here  # Optional
   ```

4. **Start services:**
   ```bash
   docker-compose up -d
   ```

5. **Verify installation:**
   ```bash
   # Check container status
   docker-compose ps
   
   # Check logs
   docker-compose logs -f
   
   # Test health endpoint
   curl http://localhost:8000/api/health
   ```

### Method 2: Individual Docker Containers

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

### Method 3: Manual Installation (Without Docker)

1. **Install Python 3.11+ and Node.js 18+**
2. **Install backend dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. **Install frontend dependencies:**
   ```bash
   cd frontend
   npm install
   ```
4. **Configure environment variables** (see Configuration section)
5. **Start services** (see System Configuration section)

## System Configuration

### Backend Configuration

**Location:** `backend/.env`

**Required Configuration:**
- `GOOGLE_API_KEY`: Google Gemini API key (required)

**Optional Configuration:**
- `OPENAI_API_KEY`: OpenAI API key (for better embeddings)
- `HOST`: Server host (default: `0.0.0.0`)
- `PORT`: Server port (default: `8000`)
- `LOG_LEVEL`: Logging level (default: `INFO`)

**Example configuration:**
```env
GOOGLE_API_KEY=AIzaSy...
OPENAI_API_KEY=sk-...
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
```

### Frontend Configuration

Frontend is a static build and doesn't require runtime configuration. API endpoint is configured in the React application source code.

### Port Configuration

**Default ports:**
- Backend API: `8000`
- Frontend: `80` (Docker) or `3000` (development)

**Changing ports:**

For Docker Compose, edit `docker-compose.yml`:
```yaml
services:
  backend:
    ports:
      - "8000:8000"  # Change first number to desired host port
  frontend:
    ports:
      - "80:80"  # Change first number to desired host port
```

## User Management

This application does not include built-in user management. All users have equal access to all features.

**Security considerations:**
- API keys should be kept secure
- Consider implementing authentication if deploying to production
- Use HTTPS in production environments
- Restrict access to admin endpoints if added

## Backup and Restore Procedures

### Backup

**Important data to backup:**
1. **ChromaDB data**: `backend/chroma_db/` directory
2. **Uploaded documents**: `backend/uploads/` directory
3. **Configuration files**: `backend/.env`

**Backup script example:**
```bash
#!/bin/bash
BACKUP_DIR="/backup/document-chatbot-$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

# Backup ChromaDB
cp -r backend/chroma_db $BACKUP_DIR/

# Backup uploads
cp -r backend/uploads $BACKUP_DIR/

# Backup configuration
cp backend/.env $BACKUP_DIR/

# Create archive
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR
```

### Restore

1. **Stop services:**
   ```bash
   docker-compose down
   ```

2. **Restore data:**
   ```bash
   # Extract backup
   tar -xzf backup.tar.gz
   
   # Restore ChromaDB
   cp -r backup/chroma_db backend/
   
   # Restore uploads
   cp -r backup/uploads backend/
   
   # Restore configuration
   cp backup/.env backend/
   ```

3. **Start services:**
   ```bash
   docker-compose up -d
   ```

## System Maintenance

### Updating the Application

1. **Pull latest changes:**
   ```bash
   git pull origin main
   ```

2. **Rebuild and restart:**
   ```bash
   docker-compose down
   docker-compose build --no-cache
   docker-compose up -d
   ```

### Monitoring

**Check service status:**
```bash
docker-compose ps
```

**View logs:**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

**Health checks:**
```bash
# Backend health
curl http://localhost:8000/api/health

# Frontend health (if configured)
curl http://localhost/health
```

### Disk Space Management

**Clean up unused Docker resources:**
```bash
docker system prune -a
```

**Clean up old uploads:**
```bash
# Remove files older than 30 days
find backend/uploads -type f -mtime +30 -delete
```

**ChromaDB cleanup:**
ChromaDB data grows with document uploads. Monitor `backend/chroma_db/` directory size.

## Troubleshooting

### Backend Issues

**Problem: API key errors**
- **Solution**: Verify `.env` file exists and contains valid `GOOGLE_API_KEY`
- **Check**: `docker-compose logs backend` for error messages

**Problem: Port already in use**
- **Solution**: Change port in `docker-compose.yml` or stop conflicting service
- **Check**: `netstat -tulpn | grep 8000` (Linux) or `lsof -i :8000` (macOS)

**Problem: Permission errors**
- **Solution**: Ensure Docker has permissions to access `uploads/` and `chroma_db/` directories
- **Fix**: `sudo chown -R $USER:$USER backend/uploads backend/chroma_db`

**Problem: Container won't start**
- **Solution**: Check logs: `docker-compose logs backend`
- **Check**: Verify Docker is running: `docker ps`

### Frontend Issues

**Problem: Cannot connect to backend**
- **Solution**: Verify backend is running and accessible
- **Check**: Backend URL in frontend configuration
- **Check**: CORS settings in backend

**Problem: Build failures**
- **Solution**: Clear npm cache: `npm cache clean --force`
- **Check**: Node.js version (requires 18+)

### General Issues

**Problem: Services not starting**
- **Solution**: Check Docker daemon: `docker info`
- **Solution**: Check disk space: `df -h`
- **Solution**: Check system resources: `free -h` (Linux)

**Problem: Slow performance**
- **Solution**: Increase allocated resources (CPU, RAM)
- **Solution**: Check network connectivity for API calls
- **Solution**: Monitor ChromaDB size and optimize if needed

## Security Settings

### Production Security Checklist

- [ ] Use HTTPS (configure reverse proxy with SSL/TLS)
- [ ] Secure API keys (use secrets management, not plain text)
- [ ] Restrict network access (firewall rules)
- [ ] Regular security updates
- [ ] Monitor logs for suspicious activity
- [ ] Implement rate limiting (if needed)
- [ ] Use strong passwords for any admin interfaces
- [ ] Regular backups

### API Key Security

**Best practices:**
- Never commit `.env` files to version control
- Use environment variables in production
- Rotate API keys regularly
- Use different keys for staging and production
- Monitor API key usage

### Network Security

**Firewall recommendations:**
- Only expose necessary ports (80, 443, 8000)
- Restrict backend API access to frontend only
- Use VPN or private networks for admin access

## Performance Tuning

### Backend Optimization

- **Increase workers**: Modify uvicorn workers in startup script
- **Database optimization**: Monitor ChromaDB performance
- **Caching**: Consider implementing response caching

### Frontend Optimization

- **Build optimization**: Use production build (`npm run build`)
- **CDN**: Serve static assets from CDN
- **Compression**: Enable gzip compression (nginx)

## Support and Resources

**Documentation:**
- [README.md](README.md) - General project information
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment instructions
- [CONFIGURATION.md](CONFIGURATION.md) - Configuration details
- [ENVIRONMENT.md](ENVIRONMENT.md) - Environment setup
- [LOGGING.md](LOGGING.md) - Logging configuration

**Troubleshooting:**
- Check application logs
- Review Docker container logs
- Verify configuration files
- Test API endpoints

**Contact:**
For issues or questions, refer to project documentation or contact the development team.
