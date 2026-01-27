#!/usr/bin/env python3
"""
Ryde Council Waste Collection API Validation Script

This script validates the new API-based approach to replace screen scraping.

New APIs:
1. Address Search: https://www.ryde.nsw.gov.au/api/v1/myarea/search?keywords={address}
2. Waste Schedule: https://www.ryde.nsw.gov.au/ocapi/Public/myarea/wasteservices?geolocationid={id}&ocsvclang=en-AU
"""

import requests
import json
import re
from html import unescape
from datetime import datetime


def search_address(address):
    """Search for an address and return the geolocation ID."""
    url = "https://www.ryde.nsw.gov.au/api/v1/myarea/search"
    params = {"keywords": address}
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    data = response.json()
    
    if data.get("Items") and len(data["Items"]) > 0:
        # Return the first (highest scoring) result
        first_result = data["Items"][0]
        return {
            "id": first_result["Id"],
            "address": first_result["AddressSingleLine"],
            "ward": first_result["MunicipalSubdivision"],
            "score": first_result["Score"]
        }
    
    return None


def get_waste_schedule(geolocation_id):
    """Get waste collection schedule for a geolocation ID."""
    url = "https://www.ryde.nsw.gov.au/ocapi/Public/myarea/wasteservices"
    params = {
        "geolocationid": geolocation_id,
        "ocsvclang": "en-AU"
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    data = response.json()
    
    if not data.get("success"):
        return None
    
    # Parse HTML content to extract waste collection dates
    html_content = unescape(data["responseContent"])
    
    schedule = {}
    
    # Extract General Waste date
    general_match = re.search(r'<h3>General Waste</h3>.*?<div class="next-service">\s*(.+?)\s*</div>', html_content, re.DOTALL)
    if general_match:
        schedule["general_waste"] = general_match.group(1).strip()
    
    # Extract Garden Organics date
    garden_match = re.search(r'<h3>Garden Organics</h3>.*?<div class="next-service">\s*(.+?)\s*</div>', html_content, re.DOTALL)
    if garden_match:
        schedule["garden_organics"] = garden_match.group(1).strip()
    
    # Extract Recycling date
    recycling_match = re.search(r'<h3>Recycling</h3>.*?<div class="next-service">\s*(.+?)\s*</div>', html_content, re.DOTALL)
    if recycling_match:
        schedule["recycling"] = recycling_match.group(1).strip()
    
    return schedule


def validate_address(address):
    """Validate a single address and print results."""
    print(f"\n{'='*60}")
    print(f"Testing: {address}")
    print(f"{'='*60}")
    
    # Step 1: Search for address
    print(f"\n1. Searching for address...")
    result = search_address(address)
    
    if not result:
        print(f"   ❌ Address not found")
        return False
    
    print(f"   ✓ Found: {result['address']}")
    print(f"   ✓ ID: {result['id']}")
    print(f"   ✓ Ward: {result['ward']}")
    print(f"   ✓ Match Score: {result['score']:.2f}")
    
    # Step 2: Get waste schedule
    print(f"\n2. Fetching waste collection schedule...")
    schedule = get_waste_schedule(result['id'])
    
    if not schedule:
        print(f"   ❌ Failed to retrieve schedule")
        return False
    
    print(f"   ✓ General Waste: {schedule.get('general_waste', 'N/A')}")
    print(f"   ✓ Garden Organics: {schedule.get('garden_organics', 'N/A')}")
    print(f"   ✓ Recycling: {schedule.get('recycling', 'N/A')}")
    
    return True


def main():
    """Main validation function."""
    print("Ryde Council Waste Collection API Validation")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test addresses
    test_addresses = [
        "54 North Road, Ryde",
        "32 Marilyn Street, North Ryde"
    ]
    
    results = []
    for address in test_addresses:
        success = validate_address(address)
        results.append((address, success))
    
    # Summary
    print(f"\n{'='*60}")
    print("VALIDATION SUMMARY")
    print(f"{'='*60}")
    
    for address, success in results:
        status = "✓ PASS" if success else "❌ FAIL"
        print(f"{status}: {address}")
    
    all_passed = all(success for _, success in results)
    
    if all_passed:
        print(f"\n✅ All tests passed! API approach is validated.")
    else:
        print(f"\n⚠️  Some tests failed. Review output above.")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit(main())
