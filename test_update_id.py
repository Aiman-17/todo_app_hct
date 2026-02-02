#!/usr/bin/env python3
"""Quick test for update by ID"""

import requests

BASE_URL = "http://localhost:8000"
TEST_USER = {"email": "chatbot.test@example.com", "password": "TestPassword123!"}

# Login
response = requests.post(f"{BASE_URL}/api/auth/login", json=TEST_USER)
token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Reset rate limiter
requests.post(f"{BASE_URL}/api/admin/reset-rate-limit")

# Test update by ID
print("\n🧪 Testing: 'update id 86 to final title'")
response = requests.post(
    f"{BASE_URL}/api/chat",
    headers=headers,
    json={"message": "update id 86 to final title"}
)

data = response.json()
print(f"Intent: {data['intent']}")
print(f"Response: {data['response']}")

if data['intent'] == 'update_task':
    print("✅ PASS: Intent correctly identified as update_task")
else:
    print(f"❌ FAIL: Intent is {data['intent']}")

# Verify
response = requests.post(
    f"{BASE_URL}/api/chat",
    headers=headers,
    json={"message": "show my tasks"}
)
print(f"\nTasks after update:\n{response.json()['response']}")
