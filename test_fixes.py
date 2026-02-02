#!/usr/bin/env python3
"""Quick test of critical bug fixes"""

import requests
import json
import sys
sys.path.insert(0, 'backend')

BASE_URL = "http://localhost:8000"
TEST_USER = {
    "email": "chatbot.test@example.com",
    "password": "TestPassword123!",
}

def test_fixes():
    # Reset rate limiter before testing
    reset_response = requests.post(f"{BASE_URL}/api/admin/reset-rate-limit")
    print(f"✓ Rate limiter reset: {reset_response.json()['message']}\n")

    # Login
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json=TEST_USER
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

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

    print("="*80)
    print("🧪 TESTING CRITICAL FIXES")
    print("="*80)

    # Create test tasks
    print("\n📝 Creating test tasks...")
    chat("Add task go to gym")
    chat("Add task test the bot")
    chat("Add task buy groceries")

    # List tasks to see IDs
    result = chat("Show my tasks")
    print(f"\nCurrent tasks:\n{result['response']}\n")

    print("\n🔴 TEST 1: Fuzzy Match - Missing Word 'to'")
    print("Input: 'delete task go gym' (task: 'go to gym')")
    result = chat("delete task go gym")
    if "deleted" in result["response"].lower() or "removed" in result["response"].lower():
        print(f"✅ PASS: {result['response'][:80]}")
    else:
        print(f"❌ FAIL: {result['response'][:80]}")

    print("\n🔴 TEST 2: Fuzzy Match - Missing Word 'the'")
    print("Input: 'complete test bot' (task: 'test the bot')")
    result = chat("complete test bot")
    if "marked" in result["response"].lower() or "completed" in result["response"].lower():
        print(f"✅ PASS: {result['response'][:80]}")
    else:
        print(f"❌ FAIL: {result['response'][:80]}")

    print("\n🔴 TEST 3: Typo Tolerance")
    print("Input: 'shw my tsks'")
    result = chat("shw my tsks")
    if "task" in result["response"].lower() and result["intent"] == "list_tasks":
        print(f"✅ PASS: Intent={result['intent']}, Response={result['response'][:80]}")
    else:
        print(f"❌ FAIL: Intent={result['intent']}, Response={result['response'][:80]}")

    print("\n🔴 TEST 4: No-Keyword Intent (Buy milk)")
    print("Input: 'Buy milk'")
    result = chat("Buy milk")
    if result["intent"] == "create_task":
        print(f"✅ PASS: Intent={result['intent']}, Response={result['response'][:80]}")
    else:
        print(f"❌ FAIL: Intent={result['intent']}, Response={result['response'][:80]}")

    print("\n🔴 TEST 5: No-Keyword Intent (I need to remember)")
    print("Input: 'I need to remember to pay bills'")
    result = chat("I need to remember to pay bills")
    if result["intent"] == "create_task":
        print(f"✅ PASS: Intent={result['intent']}, Response={result['response'][:80]}")
    else:
        print(f"❌ FAIL: Intent={result['intent']}, Response={result['response'][:80]}")

    print("\n🔴 TEST 6: No-Keyword Intent (What's pending)")
    print("Input: 'Whats pending'")
    result = chat("Whats pending")
    if result["intent"] == "list_tasks":
        print(f"✅ PASS: Intent={result['intent']}, Response={result['response'][:80]}")
    else:
        print(f"❌ FAIL: Intent={result['intent']}, Response={result['response'][:80]}")

    print("\n" + "="*80)

if __name__ == "__main__":
    test_fixes()
