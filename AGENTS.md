# AGENTS.md

## Cursor Cloud specific instructions

### Overview

This is a **Home Assistant custom integration** (HACS-compatible) called "Ryde Waste Collection". It provides sensor entities that track waste collection schedules for addresses in the City of Ryde (NSW, Australia) by polling public Ryde Council APIs.

The codebase is pure Python with no build system, no tests, no CI, no `requirements.txt`, and no `Dockerfile`. All dependencies (`homeassistant`, `requests`, `voluptuous`) are installed via pip as part of the Home Assistant package.

### Running the integration locally

1. **Install HA**: `pip install homeassistant ruff` (HA bundles `requests` and `voluptuous`).
2. **Create a config directory** (e.g. `~/ha-config`) with a minimal `configuration.yaml`:
   ```yaml
   homeassistant:
     name: "Dev Home"
     unit_system: metric
     time_zone: "Australia/Sydney"
     latitude: -33.8166
     longitude: 151.1003
   http:
     server_port: 8123
   logger:
     default: info
     logs:
       custom_components.ryde_waste_collection: debug
   ```
   Do **not** include `default_config:` — it pulls in many built-in integrations that require extra native dependencies (`pyspeex-noise`, `mutagen`, etc.) and will slow startup.
3. **Symlink the component**: `ln -sf /workspace/custom_components/ryde_waste_collection ~/ha-config/custom_components/ryde_waste_collection`
4. **Start Home Assistant**: `hass -c ~/ha-config`
5. **Complete onboarding** at `http://localhost:8123` (create user, skip defaults).
6. **Add the integration** via Settings → Devices & Services → Add Integration → "Ryde Waste Collection", or via the config entries API.
7. Use a Ryde LGA address (e.g. `129 Blaxland Road Ryde 2112`). The integration will resolve it and create 3 sensors: General Waste, Recycling, Garden Organics.

### Linting

- `ruff check custom_components/ryde_waste_collection/` — must pass with zero issues.
- `python3 -m py_compile <file>` for syntax checks.

### Key gotchas

- The integration requires **internet access** to `https://www.ryde.nsw.gov.au` — it makes live HTTP calls to two public APIs (address search + waste services). Without network access, the integration will fail to load.
- There are **no automated tests** in this repository. Validation is done manually through the HA UI or API.
- The `manifest.json` has an empty `requirements` field — the integration relies on packages bundled with Home Assistant core.
- Python 3.12 works but HA 2025.1.x warns about deprecation; Python 3.13 is preferred by later HA versions.
