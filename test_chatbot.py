#!/usr/bin/env python3
"""
Chatbot Test Script - Validates all requirements from hackathon spec.

Tests:
1. Natural language commands
2. Memory persistence (10+ messages)
3. Task recognition without exact match
4. Intent understanding without keywords
5. Typo tolerance
6. Conversation flow (stateless + history)
"""

import requests
import json
import time
from typing import Dict, Any, Optional

# Configuration
BASE_URL = "http://localhost:8000"
TEST_USER = {
    "email": "chatbot.test@example.com",
    "password": "TestPassword123!",
    "name": "Chatbot Tester"
}

class ChatbotTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.token = None
        self.conversation_id = None
        self.test_results = []

    def signup(self):
        """Create test user account."""
        response = requests.post(
            f"{self.base_url}/api/auth/signup",
            json=TEST_USER
        )
        if response.status_code == 201:
            print("✓ Test user created successfully")
            return True
        elif response.status_code == 400 and "already exists" in response.text.lower():
            print("ℹ Test user already exists, proceeding with login")
            return True
        else:
            print(f"✗ Failed to create test user: {response.status_code} - {response.text}")
            return False

    def login(self):
        """Login and get JWT token."""
        response = requests.post(
            f"{self.base_url}/api/auth/login",
            json={"email": TEST_USER["email"], "password": TEST_USER["password"]}
        )
        if response.status_code == 200:
            data = response.json()
            self.token = data.get("access_token")
            print(f"✓ Login successful, token: {self.token[:20]}...")
            return True
        else:
            print(f"✗ Login failed: {response.status_code} - {response.text}")
            return False

    def chat(self, message: str, expected_intent: Optional[str] = None, expected_success: Optional[bool] = None) -> Dict[str, Any]:
        """Send a chat message and return response."""
        headers = {"Authorization": f"Bearer {self.token}"}
        payload = {"message": message}
        if self.conversation_id:
            payload["conversation_id"] = self.conversation_id

        response = requests.post(
            f"{self.base_url}/api/chat",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            data = response.json()
            self.conversation_id = data.get("conversation_id")

            # Validate expectations
            result = {
                "message": message,
                "response": data.get("response"),
                "intent": data.get("intent"),
                "success": data.get("success"),
                "conversation_id": data.get("conversation_id"),
                "passed": True,
                "failures": []
            }

            if expected_intent and data.get("intent") != expected_intent:
                result["passed"] = False
                result["failures"].append(f"Expected intent '{expected_intent}', got '{data.get('intent')}'")

            if expected_success is not None and data.get("success") != expected_success:
                result["passed"] = False
                result["failures"].append(f"Expected success={expected_success}, got {data.get('success')}")

            self.test_results.append(result)
            return result
        else:
            error_result = {
                "message": message,
                "response": response.text,
                "intent": "ERROR",
                "success": False,
                "passed": False,
                "failures": [f"HTTP {response.status_code}: {response.text}"]
            }
            self.test_results.append(error_result)
            return error_result

    def print_result(self, result: Dict[str, Any]):
        """Print test result with formatting."""
        status = "✓" if result["passed"] else "✗"
        print(f"\n{status} Test: {result['message']}")
        print(f"  Intent: {result['intent']}")
        print(f"  Response: {result['response'][:100]}...")
        if not result["passed"]:
            for failure in result["failures"]:
                print(f"  ❌ {failure}")

    def run_tests(self):
        """Execute all test scenarios."""
        print("\n" + "="*80)
        print("🤖 CHATBOT TEST SUITE - HACKATHON VALIDATION")
        print("="*80)

        # Setup
        if not self.signup():
            return False
        if not self.login():
            return False

        print("\n" + "-"*80)
        print("TEST CATEGORY 1: Natural Language Commands (Deliverables)")
        print("-"*80)

        # Test 1.1: Task Creation
        tests = [
            ("Add a task to buy groceries", "create_task", True),
            ("I need to remember to pay bills", "create_task", True),
            ("Remind me to call mom tomorrow", "create_task", True),
            ("Buy milk", "create_task", True),  # No keyword
        ]

        for msg, intent, success in tests:
            result = self.chat(msg, intent, success)
            self.print_result(result)
            time.sleep(0.5)

        # Test 1.2: Task Listing
        print("\n--- Task Listing ---")
        tests = [
            ("Show me all my tasks", "list_tasks", True),
            ("What's pending?", "list_tasks", True),
            ("What have I completed?", "list_tasks", True),
        ]

        for msg, intent, success in tests:
            result = self.chat(msg, intent, success)
            self.print_result(result)
            time.sleep(0.5)

        print("\n" + "-"*80)
        print("TEST CATEGORY 2: Memory Persistence (10+ Messages)")
        print("-"*80)

        # Create 10 tasks to build history
        for i in range(10):
            result = self.chat(f"Add task number {i+1}", "create_task", True)
            print(f"  Message {i+1}: {result['response'][:60]}...")
            time.sleep(0.3)

        # Now test if history is preserved
        result = self.chat("Show my tasks", "list_tasks", True)
        self.print_result(result)
        task_count = result["response"].count("ID:")
        if task_count >= 10:
            print(f"  ✓ Memory test PASSED: Found {task_count} tasks")
        else:
            print(f"  ✗ Memory test FAILED: Only found {task_count} tasks (expected 10+)")

        print("\n" + "-"*80)
        print("TEST CATEGORY 3: Task Recognition WITHOUT Exact Match")
        print("-"*80)

        # First, create specific test tasks
        self.chat("Add task go to gym", "create_task", True)
        self.chat("Add task test the bot", "create_task", True)
        self.chat("Add task jhf", "create_task", True)
        time.sleep(0.5)

        # Get task list to find IDs
        list_result = self.chat("Show my tasks", "list_tasks", True)
        print(f"\nCurrent tasks:\n{list_result['response']}\n")

        # Now test fuzzy matching (CRITICAL TESTS)
        print("\n🔴 CRITICAL TEST: Fuzzy Task Matching")

        critical_tests = [
            ("delete task go gym", "delete_task", "Missing 'to' - should still match 'go to gym'"),
            ("remove gym task", "delete_task", "Partial match - should find 'go to gym'"),
            ("mark test the bot done", "complete_task", "Must preserve 'the' in matching"),
            ("complete test bot", "complete_task", "Partial match - should find 'test the bot'"),
        ]

        for msg, intent, description in critical_tests:
            print(f"\nTest: {msg}")
            print(f"Expected: {description}")
            result = self.chat(msg, intent, None)

            # Check if it failed with "not found" message
            if "not found" in result["response"].lower() or "couldn't find" in result["response"].lower():
                print(f"  ❌ FAILED: {result['response']}")
            else:
                print(f"  ✓ PASSED: {result['response'][:80]}...")
            time.sleep(0.5)

        print("\n" + "-"*80)
        print("TEST CATEGORY 4: Intent Without Keywords")
        print("-"*80)

        tests = [
            ("Whats my pending tasks", "list_tasks", "No 'show' keyword"),
            ("I'm done with the gym", None, "Should ask for clarification"),
        ]

        for msg, intent, description in tests:
            print(f"\nTest: {msg} ({description})")
            result = self.chat(msg, intent, None)
            self.print_result(result)
            time.sleep(0.5)

        print("\n" + "-"*80)
        print("TEST CATEGORY 5: Typo Tolerance")
        print("-"*80)

        typo_tests = [
            ("shw my tsks", "list_tasks", "Typos in 'show my tasks'"),
            ("ad tsk buy milk", "create_task", "Typos in 'add task'"),
            ("dlete tsk 1", "delete_task", "Typo in 'delete task'"),
        ]

        for msg, intent, description in typo_tests:
            print(f"\nTest: {msg} ({description})")
            result = self.chat(msg, intent, None)
            self.print_result(result)
            time.sleep(0.5)

        # Generate report
        self.generate_report()

    def generate_report(self):
        """Generate final test report."""
        print("\n" + "="*80)
        print("📊 FINAL TEST REPORT")
        print("="*80)

        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r["passed"])
        failed = total - passed

        print(f"\nTotal Tests: {total}")
        print(f"✓ Passed: {passed}")
        print(f"✗ Failed: {failed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")

        if failed > 0:
            print("\n❌ Failed Tests:")
            for result in self.test_results:
                if not result["passed"]:
                    print(f"  - {result['message']}")
                    for failure in result["failures"]:
                        print(f"    • {failure}")

        print("\n" + "="*80)

if __name__ == "__main__":
    tester = ChatbotTester()
    tester.run_tests()
