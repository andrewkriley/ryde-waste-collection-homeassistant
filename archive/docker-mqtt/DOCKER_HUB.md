# Docker Hub Publishing

This project automatically builds and publishes Docker images to Docker Hub using GitHub Actions.

## Published Image

**Docker Hub:** `andreril/ryde-waste-collection`

### Available Tags

- `latest` - Latest build from main branch
- `main` - Latest build from main branch
- `v1.0.0` - Semantic version tags (when tagged)
- `1.0` - Major.minor version
- `1` - Major version

## Using Pre-built Images

The default `docker-compose.yml` uses the pre-built image from Docker Hub:

```yaml
services:
  ryde-waste-collection:
    image: andreril/ryde-waste-collection:latest
```

Simply run:
```bash
docker-compose up -d
```

No build step required! The image will be automatically downloaded from Docker Hub.

## Local Development

For local development and testing changes, use the dev compose file:

```bash
# Build and run locally
docker-compose -f docker-compose.dev.yml up -d

# Rebuild after changes
docker-compose -f docker-compose.dev.yml up -d --build
```

## GitHub Actions Workflow

The workflow (`.github/workflows/docker-build-publish.yml`) automatically:

1. **Builds** multi-platform images (amd64, arm64)
2. **Pushes** to Docker Hub on:
   - Push to `main` branch → `latest` and `main` tags
   - Push to version tags (`v*`) → versioned tags
   - Push to `docker-hub-publish` branch (for testing)
3. **Uses layer caching** for faster builds

### Required Secrets

Set these in your GitHub repository settings (Settings → Secrets → Actions):

- `DOCKER_USERNAME` - Your Docker Hub username
- `DOCKER_PASSWORD` - Docker Hub access token (recommended) or password

### Creating Docker Hub Access Token

1. Go to https://hub.docker.com/settings/security
2. Click "New Access Token"
3. Name it (e.g., "GitHub Actions")
4. Copy the token and save it as `DOCKER_PASSWORD` secret in GitHub

## Manual Docker Hub Push

To manually push to Docker Hub:

```bash
# Login
docker login -u andreril

# Build for multiple platforms
docker buildx build --platform linux/amd64,linux/arm64 \
  -t andreril/ryde-waste-collection:latest \
  -t andreril/ryde-waste-collection:v1.0.0 \
  --push .
```

## Versioning

To create a new version:

```bash
# Tag the commit
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# GitHub Actions will automatically build and push:
# - andreril/ryde-waste-collection:v1.0.0
# - andreril/ryde-waste-collection:1.0
# - andreril/ryde-waste-collection:1
# - andreril/ryde-waste-collection:latest (if on main)
```

## Image Size

The published image is optimized:
- Multi-stage build
- Debian slim base
- Layer caching
- Approximate size: ~500MB

## Supported Platforms

- `linux/amd64` - x86_64 (Intel/AMD)
- `linux/arm64` - ARM64 (Raspberry Pi 4+, Apple Silicon)

## Troubleshooting

### Pull Rate Limits

Docker Hub has pull rate limits:
- Anonymous: 100 pulls per 6 hours
- Authenticated: 200 pulls per 6 hours
- Pro/Team: Unlimited

To avoid limits, login:
```bash
docker login
```

### Using Specific Version

Pin to a specific version in production:
```yaml
services:
  ryde-waste-collection:
    image: andreril/ryde-waste-collection:v1.0.0  # Pinned version
```

### Checking Available Tags

```bash
# List all tags
curl -s https://registry.hub.docker.com/v2/repositories/andreril/ryde-waste-collection/tags/ | jq -r '.results[].name'
```
