# Ryde Council Waste Collection - API Validation

## Overview
This document validates the new API-based approach to replace the current screen scraping method for retrieving waste collection schedules from Ryde Council.

## New API Endpoints

### 1. Address Search API
**Endpoint:** `https://www.ryde.nsw.gov.au/api/v1/myarea/search`

**Method:** GET

**Parameters:**
- `keywords` (string): The address to search for

**Example Request:**
```
https://www.ryde.nsw.gov.au/api/v1/myarea/search?keywords=54+North+Road%2C+Ryde
```

**Response Format:**
```json
{
  "Items": [
    {
      "Id": "d681a13e-bf24-498e-b3df-f7e6796eee8f",
      "AddressSingleLine": "54 North Road, Ryde 2112",
      "MunicipalSubdivision": "Central Ward",
      "Distance": 0,
      "Score": 18.723524,
      "LatLon": null
    }
  ],
  "Offset": 0,
  "Limit": 10,
  "Total": 10
}
```

**Notes:**
- Returns multiple potential matches ranked by Score
- First result (highest score) is typically the correct match
- `Id` field is required for the waste services API

### 2. Waste Services API
**Endpoint:** `https://www.ryde.nsw.gov.au/ocapi/Public/myarea/wasteservices`

**Method:** GET

**Parameters:**
- `geolocationid` (string): The ID from the address search API
- `ocsvclang` (string): Language parameter (use "en-AU")

**Example Request:**
```
https://www.ryde.nsw.gov.au/ocapi/Public/myarea/wasteservices?geolocationid=d681a13e-bf24-498e-b3df-f7e6796eee8f&ocsvclang=en-AU
```

**Response Format:**
```json
{
  "success": true,
  "responseContent": "<div>...HTML content with waste collection dates...</div>"
}
```

**Notes:**
- Response contains HTML that needs to be parsed
- HTML includes dates for General Waste, Garden Organics, and Recycling
- Date format: "Day DD/M/YYYY" (e.g., "Wed 28/1/2026")

## Validation Results

### Test Address 1: 54 North Road, Ryde
- ✅ **Address Found:** 54 North Road, Ryde 2112
- ✅ **Geolocation ID:** d681a13e-bf24-498e-b3df-f7e6796eee8f
- ✅ **Ward:** Central Ward
- ✅ **Schedule Retrieved:**
  - General Waste: Wed 28/1/2026
  - Garden Organics: Wed 28/1/2026
  - Recycling: Wed 4/2/2026

### Test Address 2: 32 Marilyn Street, North Ryde
- ✅ **Address Found:** 32 Marilyn Street, North Ryde 2113
- ✅ **Geolocation ID:** 82a9e578-871b-4559-88b1-0406ae3d1089
- ✅ **Ward:** East Ward
- ✅ **Schedule Retrieved:**
  - General Waste: Fri 30/1/2026
  - Garden Organics: Fri 30/1/2026
  - Recycling: Fri 6/2/2026

## Advantages Over Screen Scraping

1. **More Reliable:** API endpoints are less likely to break with website redesigns
2. **Cleaner Data:** JSON response format is easier to parse than HTML
3. **Better Performance:** Direct API calls are faster than full page scraping
4. **Official Support:** Using public APIs that Ryde Council's website uses internally
5. **Structured Data:** Address search returns normalized address data with geolocation IDs

## Implementation Notes

### Python Example
See `api_validation.py` for a complete working example that:
- Searches for an address
- Retrieves the geolocation ID
- Fetches the waste collection schedule
- Parses the HTML response to extract dates

### Dependencies
- `requests` library for HTTP requests
- Standard library modules: `json`, `re`, `html`, `datetime`

### Parsing Logic
The waste services API returns HTML content that must be parsed:
```python
import re
from html import unescape

html_content = unescape(response_content)
general_waste = re.search(
    r'<h3>General Waste</h3>.*?<div class="next-service">\s*(.+?)\s*</div>',
    html_content,
    re.DOTALL
).group(1).strip()
```

## Running the Validation Script

```bash
python3 api_validation.py
```

This will test both addresses and display detailed results.

## Conclusion

✅ **API Validation: SUCCESSFUL**

Both test addresses successfully returned accurate waste collection schedules. The new API approach is validated and ready for implementation to replace the screen scraping method.

## Next Steps

1. Refactor existing scraper to use the new API endpoints
2. Update error handling for API-specific edge cases
3. Consider caching geolocation IDs for frequently queried addresses
4. Update tests to validate API integration
5. Monitor API stability and response times in production
