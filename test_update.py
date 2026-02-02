#!/usr/bin/env python3
"""Test update command functionality"""

import requests
import json

BASE_URL = "http://localhost:8000"
TEST_USER = {
    "email": "chatbot.test@example.com",
    "password": "TestPassword123!",
}

def test_update():
    # Login
    response = requests.post(f"{BASE_URL}/api/auth/login", json=TEST_USER)
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Reset rate limiter
    requests.post(f"{BASE_URL}/api/admin/reset-rate-limit")

    conversation_id = None

    def chat(msg):
        nonlocal conversation_id
        payload = {"message": msg}
        if conversation_id:
            payload["conversation_id"] = conversation_id

        response = requests.post(
            f"{BASE_URL}/api/chat",
            headers=headers,
            json=payload
        )
        data = response.json()
        conversation_id = data.get("conversation_id")
        return data

    print("=" * 80)
    print("🧪 TESTING UPDATE FUNCTIONALITY")
    print("=" * 80)

    # Create a test task
    print("\n📝 Step 1: Creating test task...")
    result = chat("Add task fix rearching typo")
    print(f"Response: {result['response']}")
    print(f"Intent: {result['intent']}")

    # Get the task ID
    result = chat("Show my tasks")
    print(f"\nCurrent tasks:\n{result['response']}\n")

    # Test 1: Update by task reference
    print("\n🔴 TEST 1: Update by task reference")
    print("Input: 'update rearching to researching'")
    result = chat("update rearching to researching")
    print(f"Intent: {result['intent']}")
    print(f"Response: {result['response']}")

    if result['intent'] == 'update_task':
        print("✅ PASS: Intent correctly identified as update_task")
    else:
        print(f"❌ FAIL: Intent is {result['intent']}, expected update_task")

    # Verify the update worked
    print("\n📋 Verifying update...")
    result = chat("Show my tasks")
    if "researching" in result['response']:
        print("✅ PASS: Task title updated successfully")
    else:
        print("❌ FAIL: Task title not updated")
    print(f"Current tasks:\n{result['response']}\n")

    # Test 2: Update by task ID (need to get a task ID first)
    print("\n🔴 TEST 2: Update by task ID")
    result = chat("Add task test task for id update")

    # Extract task ID from response
    import re
    match = re.search(r'ID: (\d+)', result['response'])
    if match:
        task_id = match.group(1)
        print(f"Created task ID: {task_id}")

        print(f"Input: 'update id {task_id} to updated via ID'")
        result = chat(f"update id {task_id} to updated via ID")
        print(f"Intent: {result['intent']}")
        print(f"Response: {result['response']}")

        if result['intent'] == 'update_task':
            print("✅ PASS: Intent correctly identified as update_task")
        else:
            print(f"❌ FAIL: Intent is {result['intent']}, expected update_task")

        # Verify
        result = chat("Show my tasks")
        if "updated via ID" in result['response']:
            print("✅ PASS: Task updated via ID successfully")
        else:
            print("❌ FAIL: Task not updated via ID")
        print(f"Current tasks:\n{result['response']}\n")

    print("=" * 80)

if __name__ == "__main__":
    test_update()
