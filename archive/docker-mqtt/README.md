# Docker/MQTT Installation (Archived)

This folder contains the original Docker/MQTT implementation of the Ryde Waste Collection integration.

**Note:** This method is now considered legacy. The recommended installation method is the native Home Assistant custom integration (see main README).

## Why Archived?

The project has shifted focus to the native Home Assistant custom component, which offers:
- Easier installation (no Docker/MQTT setup required)
- Better integration with Home Assistant
- UI-based configuration
- Lower resource usage

## Using These Files

If you still want to use the Docker/MQTT method:

1. Copy these files back to the project root
2. Follow the instructions in `DOCKER.md` and `MQTT.md`
3. Use `docker-compose.yml` to run the container

## Files in This Archive

- `Dockerfile` - Docker image definition
- `docker-compose.yml` - Docker Compose configuration
- `docker-compose.dev.yml` - Development Docker Compose configuration
- `entrypoint.sh` - Container entrypoint script
- `ryde_mqtt_publisher.py` - MQTT publisher script
- `ryde_waste_scraper.py` - API scraper (also used by native integration)
- `api_validation.py` - API validation script
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variables template
- `DOCKER.md` - Docker installation guide
- `DOCKER_HUB.md` - Docker Hub publishing guide
- `MQTT.md` - MQTT setup guide
- `.dockerignore` - Docker ignore file
- `homeassistant_dashboard_full.yaml` - Full dashboard YAML
- `homeassistant_mushroom_card.yaml` - Mushroom card YAML

## Migration to Native Integration

To migrate from Docker/MQTT to the native integration:

1. Stop the Docker container:
   ```bash
   docker compose down
   ```

2. Remove MQTT sensors from Home Assistant (they'll be auto-discovered sensors)

3. Install the native custom component:
   ```bash
   cd /path/to/homeassistant/custom_components
   git clone https://github.com/andrewkriley/ryde-waste-collection-homeassistant.git ryde_waste_collection
   ```

4. Restart Home Assistant

5. Add the integration via UI: Settings → Devices & Services → Add Integration → Ryde Waste Collection

See the main [INSTALLATION.md](../../INSTALLATION.md) for detailed instructions.
