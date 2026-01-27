# Logging Instructions

This document describes logging configuration, log file locations, and logging best practices for the Document Chatbot application.

## Log File Locations

### Backend Logs

**Docker Deployment:**
- **Location**: Docker container stdout/stderr
- **View**: `docker-compose logs backend` or `docker logs <container-name>`
- **Persistent logs**: Not stored on disk by default (use volume mounting for persistence)

**Manual Deployment:**
- **Location**: Application stdout/stderr
- **Redirect to file**: Configure in startup script
- **Example**: `python -m uvicorn app.main:app > backend.log 2>&1`

**Uvicorn Access Logs:**
- Uvicorn automatically logs HTTP requests
- Format: Standard HTTP access log format
- Location: stdout/stderr

### Frontend Logs

**Production (Nginx):**
- **Access logs**: `/var/log/nginx/access.log` (inside container)
- **Error logs**: `/var/log/nginx/error.log` (inside container)
- **View**: `docker-compose logs frontend` or `docker logs <container-name>`

**Development:**
- **Location**: Browser console and terminal
- **View**: Browser DevTools Console
- **Build logs**: Terminal output during `npm start`

## Logging Configuration

### Backend Logging

**Current Implementation:**
- Uses Python's built-in `logging` module
- Uvicorn handles HTTP request logging
- FastAPI provides automatic request/response logging

**Log Levels:**
- `DEBUG`: Detailed information for debugging
- `INFO`: General informational messages
- `WARNING`: Warning messages (non-critical issues)
- `ERROR`: Error messages
- `CRITICAL`: Critical errors

**Configuration:**
Set `LOG_LEVEL` in `backend/.env`:
```env
LOG_LEVEL=INFO
```

**Default Behavior:**
- If `LOG_LEVEL` not set: Uses `INFO` level
- Uvicorn default: `INFO` level
- FastAPI: Logs all requests and responses

### Frontend Logging

**Development:**
- React development mode shows detailed logs
- Browser console shows all `console.log()`, `console.error()`, etc.
- Source maps enabled for debugging

**Production:**
- Production build minimizes and removes console logs
- Only critical errors are logged
- Nginx access/error logs available

## Log Format

### Backend Log Format

**Uvicorn Access Logs:**
```
INFO:     127.0.0.1:52341 - "GET /api/health HTTP/1.1" 200 OK
INFO:     127.0.0.1:52342 - "POST /api/chat/ HTTP/1.1" 200 OK
```

**Application Logs:**
```
INFO:     Application startup complete
ERROR:    API key validation failed
WARNING:  OpenAI API unavailable, using fallback
```

**Error Stack Traces:**
```
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "...", line X, in function
    ...
```

### Frontend Log Format

**Nginx Access Logs:**
```
127.0.0.1 - - [27/Jan/2026:18:00:00 +0000] "GET / HTTP/1.1" 200 1234
```

**Nginx Error Logs:**
```
2026/01/27 18:00:00 [error] 1#1: *1 connect() failed (111: Connection refused)
```

## Log Rotation

### Docker Logs

**Docker Compose:**
Configure log rotation in `docker-compose.yml`:
```yaml
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
  frontend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

**Manual Docker:**
```bash
docker run --log-opt max-size=10m --log-opt max-file=3 ...
```

### Manual Deployment Log Rotation

**Linux (logrotate):**
Create `/etc/logrotate.d/document-chatbot`:
```
/path/to/backend.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
```

**Python logging with rotation:**
```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    'backend.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
```

## Logging Best Practices

### Development

- Use `DEBUG` level for detailed troubleshooting
- Check browser console for frontend issues
- Monitor Docker logs in real-time: `docker-compose logs -f`

### Production

- Use `INFO` or `WARNING` level (avoid `DEBUG`)
- Set up log rotation to prevent disk space issues
- Monitor logs for errors and warnings
- Store logs persistently (volume mounting or external logging service)
- Consider centralized logging (ELK stack, Splunk, etc.)

## Viewing Logs

### Docker Compose

**All services:**
```bash
docker-compose logs -f
```

**Specific service:**
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

**Last N lines:**
```bash
docker-compose logs --tail=100 backend
```

**Since specific time:**
```bash
docker-compose logs --since 2026-01-27T10:00:00 backend
```

### Docker Containers

**View logs:**
```bash
docker logs <container-name>
docker logs -f <container-name>  # Follow logs
docker logs --tail=100 <container-name>
```

### Manual Deployment

**Backend:**
```bash
# If redirected to file
tail -f backend.log

# If running in terminal
# Logs appear in terminal output
```

**Frontend:**
- Development: Browser DevTools Console
- Production: Check Nginx logs inside container

## Log Analysis

### Common Log Patterns

**Successful requests:**
```
INFO:     "GET /api/health HTTP/1.1" 200 OK
INFO:     "POST /api/chat/ HTTP/1.1" 200 OK
```

**Errors:**
```
ERROR:    API key validation failed
ERROR:    Document processing failed: FileNotFoundError
ERROR:    Connection to Gemini API failed
```

**Warnings:**
```
WARNING:  OpenAI API unavailable, using sentence-transformers
WARNING:  Large document detected, processing may take longer
```

### Searching Logs

**Docker logs:**
```bash
docker-compose logs backend | grep ERROR
docker-compose logs backend | grep -i "api key"
```

**Log files:**
```bash
grep ERROR backend.log
grep -i "failed" backend.log
tail -f backend.log | grep ERROR
```

## Troubleshooting with Logs

### Backend Issues

**Check for errors:**
```bash
docker-compose logs backend | grep -i error
```

**Check API key status:**
```bash
docker-compose logs backend | grep -i "api key"
```

**Check document processing:**
```bash
docker-compose logs backend | grep -i "document"
```

### Frontend Issues

**Check Nginx errors:**
```bash
docker-compose logs frontend | grep -i error
```

**Check access logs:**
```bash
docker-compose logs frontend | grep "GET\|POST"
```

## Log Retention

### Recommended Retention Policy

- **Development**: Keep last 7 days
- **Staging**: Keep last 30 days
- **Production**: Keep last 90 days (or as per compliance requirements)

### Disk Space Management

**Monitor log size:**
```bash
docker system df
du -sh backend/chroma_db/
du -sh backend/uploads/
```

**Clean old logs:**
```bash
# Docker logs
docker system prune

# Application logs
find /var/log -name "*.log" -mtime +30 -delete
```

## Security Considerations

### Sensitive Information

**Never log:**
- API keys
- Passwords
- Personal user data
- Full document content (use summaries)

**Current implementation:**
- API keys are not logged
- User queries may be logged (consider privacy)
- Document content is not logged in full

### Log Access Control

- Restrict log file permissions: `chmod 640 *.log`
- Use secure log storage
- Implement log access auditing
- Encrypt logs in transit and at rest (if required)

## Integration with External Logging Services

### Options

- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Splunk**
- **CloudWatch** (AWS)
- **Azure Monitor** (Azure)
- **Google Cloud Logging** (GCP)
- **Datadog**
- **New Relic**

### Example: Docker Logging Driver

```yaml
services:
  backend:
    logging:
      driver: "syslog"
      options:
        syslog-address: "tcp://logs.example.com:514"
```

## Additional Resources

- [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
- [Uvicorn Logging](https://www.uvicorn.org/settings/#logging)
- [FastAPI Logging](https://fastapi.tiangolo.com/advanced/logging/)
- [Docker Logging Drivers](https://docs.docker.com/config/containers/logging/configure/)

For more information:
- [ADMIN_GUIDE.md](ADMIN_GUIDE.md) - System administration
- [CONFIGURATION.md](CONFIGURATION.md) - Configuration details
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment instructions
