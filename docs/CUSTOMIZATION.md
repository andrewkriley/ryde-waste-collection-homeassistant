# Customization Guide

## Dynamic Icon Colors

Make your waste collection icons change color automatically as collection day approaches!

### Overview

Icons will:
- **Stay grey/blue** (default) when collection is more than 7 days away
- **Turn to bin color** when collection is 7 days or fewer away (including today!)
- Match actual Ryde Council bin colors: 🔴 Red (General), 🟡 Yellow (Recycling), 🟢 Green (Garden)

---

## Full Dashboard Example

This complete dashboard configuration uses Mushroom cards with dynamic colors. Install **Mushroom** from HACS (Frontend → Mushroom) first.

### Complete Dashboard YAML

```yaml
title: Waste Collection
views:
  - title: Home
    path: home
    cards:
      - type: vertical-stack
        cards:
          - type: custom:mushroom-title-card
            title: Waste Collection
            subtitle: Next 7 Days
            
          - type: custom:mushroom-entity-card
            entity: sensor.ryde_waste_collection_general_waste
            name: General Waste
            icon: mdi:trash-can
            icon_color: |-
              {% set days = state_attr('sensor.ryde_waste_collection_general_waste', 'days_until') | int(-1) %}
              {% if days >= 0 and days <= 7 %}
                red
              {% else %}
                grey
              {% endif %}
            primary_info: name
            secondary_info: state
            badge_icon: |-
              {% set days = state_attr('sensor.ryde_waste_collection_general_waste', 'days_until') | int(-1) %}
              {% if days >= 0 and days <= 1 %}
                mdi:alert
              {% endif %}
            badge_color: red
            tap_action:
              action: more-info
            
          - type: custom:mushroom-entity-card
            entity: sensor.ryde_waste_collection_recycling
            name: Recycling
            icon: mdi:recycle
            icon_color: |-
              {% set days = state_attr('sensor.ryde_waste_collection_recycling', 'days_until') | int(-1) %}
              {% if days >= 0 and days <= 7 %}
                yellow
              {% else %}
                grey
              {% endif %}
            primary_info: name
            secondary_info: state
            badge_icon: |-
              {% set days = state_attr('sensor.ryde_waste_collection_recycling', 'days_until') | int(-1) %}
              {% if days >= 0 and days <= 1 %}
                mdi:alert
              {% endif %}
            badge_color: yellow
            tap_action:
              action: more-info
            
          - type: custom:mushroom-entity-card
            entity: sensor.ryde_waste_collection_garden_organics
            name: Garden Organics
            icon: mdi:leaf
            icon_color: |-
              {% set days = state_attr('sensor.ryde_waste_collection_garden_organics', 'days_until') | int(-1) %}
              {% if days >= 0 and days <= 7 %}
                green
              {% else %}
                grey
              {% endif %}
            primary_info: name
            secondary_info: state
            badge_icon: |-
              {% set days = state_attr('sensor.ryde_waste_collection_garden_organics', 'days_until') | int(-1) %}
              {% if days >= 0 and days <= 1 %}
                mdi:alert
              {% endif %}
            badge_color: green
            tap_action:
              action: more-info
```

### Key Template Syntax

The critical part is using the `| int(-1)` filter:

```jinja2
{% set days = state_attr('sensor.ryde_waste_collection_general_waste', 'days_until') | int(-1) %}
{% if days >= 0 and days <= 7 %}
  red
{% else %}
  grey
{% endif %}
```

This:
- Converts `days_until` to an integer
- Uses `-1` as default if the attribute is missing or None
- Checks if days is between 0 and 7 (inclusive)

---

## Troubleshooting

### Step 1: Verify Your Sensors

Go to **Developer Tools** → **States** and find your sensors:
- `sensor.ryde_waste_collection_general_waste`
- `sensor.ryde_waste_collection_recycling`
- `sensor.ryde_waste_collection_garden_organics`

Check that each sensor has a `days_until` attribute with a number value (e.g., 0, 3, 7).

### Step 2: Test the Template

Go to **Developer Tools** → **Template** and paste:

```jinja2
{% set days = state_attr('sensor.ryde_waste_collection_general_waste', 'days_until') | int(-1) %}
Days until: {{ days }}
Days >= 0: {{ days >= 0 }}
Days <= 7: {{ days <= 7 }}
Should be colored: {{ days >= 0 and days <= 7 }}
Result: {{ 'red' if (days >= 0 and days <= 7) else 'grey' }}
```

Expected output when `days_until = 0`:
```
Days until: 0
Days >= 0: True
Days <= 7: True
Should be colored: True
Result: red
```

### Step 3: Try Alternative Templates

If the main template still doesn't work, try these alternatives:

**Option A: One-liner with range**
```yaml
icon_color: >-
  {{ 'red' if (state_attr('sensor.ryde_waste_collection_general_waste', 'days_until') | int(-1)) in range(0, 8) else 'grey' }}
```

**Option B: Using default filter**
```yaml
icon_color: >-
  {{ 'red' if (state_attr('sensor.ryde_waste_collection_general_waste', 'days_until') | default(999) | int) <= 7 else 'grey' }}
```

### Step 4: Clear Cache and Restart

1. **Clear browser cache**: Ctrl+Shift+R (or Cmd+Shift+R on Mac)
2. **Restart Home Assistant**: Settings → System → Restart
3. **Update Mushroom**: HACS → Frontend → Mushroom → Update if available

### Step 5: Check Mushroom Installation

Make sure Mushroom cards are properly installed:
1. Go to **HACS** → **Frontend**
2. Find **Mushroom** in your installed integrations
3. If not installed, click **Explore & Download Repositories**, search for **Mushroom**, and install

---

## Common Issues

### Icons Always Grey

**Cause**: The template isn't evaluating correctly or `days_until` is missing.

**Fix**: Use the `| int(-1)` filter version shown above. This is the most reliable.

### Icons Show Wrong Color

**Cause**: You may have copied the template incorrectly or there are extra spaces.

**Fix**: Copy the exact YAML from above, ensuring proper indentation.

### Sensors Don't Exist

**Cause**: Integration not configured or sensors failed to load.

**Fix**: 
1. Go to Settings → Devices & Services
2. Find "Ryde Waste Collection"
3. Click Configure and verify your address
4. Restart Home Assistant

---

## Customizing the Threshold

Change when icons become colored by adjusting the number:

**3 days notice**:
```yaml
{% if days >= 0 and days <= 3 %}
```

**14 days notice**:
```yaml
{% if days >= 0 and days <= 14 %}
```

---

## Why Use `| int(-1)`?

The `| int(-1)` filter is crucial because:
1. **Type safety**: Ensures the value is always an integer
2. **None handling**: Converts None to -1 (which is < 0, so always grey)
3. **Reliability**: Works consistently across all Home Assistant versions
4. **Range check**: `days >= 0` ensures we ignore the -1 default

This is the recommended approach for Mushroom card templates.

---

## Installing Mushroom Cards

1. Open **HACS** in Home Assistant
2. Go to **Frontend**
3. Click **Explore & Download Repositories**
4. Search for **Mushroom**
5. Click **Download**
6. Restart Home Assistant
7. Use the dashboard configuration above

---

## Color Reference

| Waste Type | When Colored | Icon Color | Otherwise |
|------------|--------------|------------|-----------|
| General Waste | 0-7 days | `red` | `grey` |
| Recycling | 0-7 days | `yellow` | `grey` |
| Garden Organics | 0-7 days | `green` | `grey` |

**Note**: `days_until = 0` means collection is **today** - it will show colored!
