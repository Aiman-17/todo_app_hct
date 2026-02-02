#!/usr/bin/env python3
"""Clean up duplicate test tasks"""

import requests

BASE_URL = "http://localhost:8000"
TEST_USER = {"email": "chatbot.test@example.com", "password": "TestPassword123!"}

# Login
response = requests.post(f"{BASE_URL}/api/auth/login", json=TEST_USER)
token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Get all tasks
response = requests.get(f"{BASE_URL}/api/tasks", headers=headers)
tasks = response.json()

# Delete all tasks
for task in tasks:
    requests.delete(f"{BASE_URL}/api/tasks/{task['id']}", headers=headers)
    print(f"Deleted: {task['title']} (ID: {task['id']})")

print(f"\n✓ Cleaned up {len(tasks)} tasks")
