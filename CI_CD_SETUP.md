# CI/CD Setup Guide for GitLab

This guide explains how to set up and configure the CI/CD pipeline for the Document Chatbot project in GitLab.

## Prerequisites

1. GitLab project with CI/CD enabled
2. GitLab Runner with Docker executor configured
3. Access to GitLab Container Registry
4. Docker-in-Docker (DinD) service available

## Initial Setup

### 1. Configure GitLab Runner

Ensure your GitLab Runner is configured with Docker executor:

```toml
[[runners]]
  name = "docker-runner"
  url = "https://gitlab.fit.cvut.cz/"
  token = "your-runner-token"
  executor = "docker"
  [runners.docker]
    image = "docker:latest"
    privileged = true
    volumes = ["/certs/client", "/cache"]
```

### 2. Set Up CI/CD Variables

Go to **Project Settings → CI/CD → Variables** and add the following variables:

#### Required Variables

- `CI_REGISTRY_USER`: GitLab registry username
- `CI_REGISTRY_PASSWORD`: GitLab registry password (masked)
- `CI_REGISTRY`: GitLab container registry URL (usually auto-set)

#### Optional Variables (for deployment)

- `DEPLOY_HOST`: Deployment server hostname
- `DEPLOY_USER`: Deployment server username
- `DEPLOY_KEY`: SSH private key for deployment (file type, masked)
- `GOOGLE_API_KEY`: Google API key (masked, protected)
- `OPENAI_API_KEY`: OpenAI API key (masked, protected)

### 3. Container Registry Setup

The pipeline automatically pushes images to GitLab Container Registry:

- Backend: `$CI_REGISTRY_IMAGE/backend:$CI_COMMIT_REF_SLUG`
- Frontend: `$CI_REGISTRY_IMAGE/frontend:$CI_COMMIT_REF_SLUG`

To view images:
1. Go to **Packages & Registries → Container Registry**
2. Images will be listed by tag

## Pipeline Stages

### Build Stage

Builds Docker images for both backend and frontend:

- **build_backend**: Builds backend Docker image
- **build_frontend**: Builds frontend Docker image

**Triggers:**
- Pushes to `main` branch
- Pushes to `develop` branch
- Tag creation

### Test Stage

Runs tests and builds:

- **test_backend**: Runs Python tests (if available)
- **test_frontend**: Runs React tests and builds production bundle

**Triggers:**
- Pushes to `main` branch
- Pushes to `develop` branch
- Merge requests

**Note:** Tests are set to `allow_failure: true` if no tests exist yet.

### Security Stage

Performs security scanning:

- **security_backend**: Scans Python dependencies for vulnerabilities
- **security_frontend**: Scans npm dependencies for vulnerabilities

**Tools Used:**
- Backend: `safety` and `pip-audit`
- Frontend: `npm audit`

**Triggers:**
- Pushes to `main` branch
- Pushes to `develop` branch
- Merge requests

### Deploy Stage

Deploys application to environments:

- **deploy_staging**: Manual deployment to staging (from `develop` branch)
- **deploy_production**: Manual deployment to production (from `main` branch or tags)

**Note:** Deployment jobs are set to `when: manual` for safety.

## Customizing the Pipeline

### Adding Tests

#### Backend Tests

1. Create `backend/tests/` directory
2. Add test files (e.g., `test_main.py`)
3. Install pytest: `pip install pytest`
4. Update `requirements.txt` if needed
5. Pipeline will automatically run tests

#### Frontend Tests

1. Create test files in `frontend/src/`
2. Tests are automatically discovered by `react-scripts test`
3. Pipeline will run tests automatically

### Customizing Deployment

Edit `.gitlab-ci.yml` and modify the deploy jobs:

```yaml
deploy_production:
  script:
    - echo "Your deployment commands here"
    # Example: kubectl apply -f k8s/
    # Example: ssh user@host "docker-compose pull && docker-compose up -d"
```

### Adding More Stages

You can add additional stages:

```yaml
stages:
  - build
  - test
  - security
  - lint
  - deploy

lint_backend:
  stage: lint
  script:
    - flake8 app/
    - black --check app/
```

## Monitoring Pipeline

### View Pipeline Status

1. Go to **CI/CD → Pipelines**
2. Click on a pipeline to see detailed job status
3. Click on a job to see logs

### Pipeline Artifacts

Frontend build artifacts are saved:
- Location: `frontend/build/`
- Expiration: 1 week
- Accessible from pipeline page

### Security Reports

Security scan results:
- View in pipeline job logs
- Check for vulnerabilities in dependencies
- Update dependencies if vulnerabilities found

## Troubleshooting

### Pipeline Fails at Build Stage

**Issue:** Docker build fails

**Solutions:**
- Check Dockerfile syntax
- Verify all files are committed
- Check `.dockerignore` files
- Verify Docker-in-Docker is configured

### Pipeline Fails at Test Stage

**Issue:** Tests fail or not found

**Solutions:**
- Tests are set to `allow_failure: true` by default
- Add tests to prevent failures
- Check test configuration

### Container Registry Access Denied

**Issue:** Cannot push to registry

**Solutions:**
- Verify `CI_REGISTRY_USER` and `CI_REGISTRY_PASSWORD` are set
- Check registry permissions
- Verify runner has access to registry

### Security Scans Show Vulnerabilities

**Issue:** Security stage reports vulnerabilities

**Solutions:**
- Review vulnerability reports
- Update affected dependencies
- Security stage is set to `allow_failure: true` by default
- Fix critical vulnerabilities before production deployment

## Best Practices

1. **Always test locally before pushing:**
   ```bash
   docker-compose build
   docker-compose up
   ```

2. **Use feature branches:**
   - Create branches for new features
   - Use merge requests for code review
   - Pipeline runs on merge requests

3. **Tag releases:**
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

4. **Monitor security scans:**
   - Regularly check for vulnerabilities
   - Update dependencies promptly
   - Review security reports

5. **Use manual deployment:**
   - Manual deployment prevents accidental releases
   - Review changes before deploying
   - Test in staging before production

## Advanced Configuration

### Parallel Jobs

Jobs in the same stage run in parallel. To limit parallelism:

```yaml
variables:
  GIT_STRATEGY: clone
```

### Caching

Add caching for faster builds:

```yaml
cache:
  paths:
    - backend/.venv/
    - frontend/node_modules/
```

### Conditional Jobs

Run jobs conditionally:

```yaml
deploy_production:
  only:
    - tags
  except:
    - /^v\d+\.\d+\.\d+-.*$/
```

## Support

For CI/CD issues:
1. Check pipeline logs
2. Verify runner configuration
3. Review GitLab CI/CD documentation
4. Check project settings
