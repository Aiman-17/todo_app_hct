#!/usr/bin/env python3
"""Test API directly to see raw responses"""

import requests
import json

BASE_URL = "http://localhost:8000"
TEST_USER = {
    "email": "chatbot.test@example.com",
    "password": "TestPassword123!",
}

# Login
response = requests.post(f"{BASE_URL}/api/auth/login", json=TEST_USER)
token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Test single case with full response
test_msg = "shw my tsks"
response = requests.post(
    f"{BASE_URL}/api/chat",
    headers=headers,
    json={"message": test_msg}
)

print(f"Input: '{test_msg}'")
print(f"\nFull API Response:")
print(json.dumps(response.json(), indent=2))
