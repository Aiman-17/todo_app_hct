#!/usr/bin/env python3
"""
Critical E2E Test Suite - Automated
Tests core functionality via API calls
Hackathon validation - Production readiness
"""

import requests
import time
import sys
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

# Test users
user1 = {
    "name": "Test User 1",
    "email": f"test1.{int(time.time())}@example.com",
    "password": "SecurePass123!"
}

user2 = {
    "name": "Test User 2",
    "email": f"test2.{int(time.time())}@example.com",
    "password": "SecurePass123!"
}

# Track results
results = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "tests": []
}

def log_test(name, passed, message=""):
    """Log test result"""
    results["total"] += 1
    if passed:
        results["passed"] += 1
        print(f"✅ PASS: {name}")
    else:
        results["failed"] += 1
        print(f"❌ FAIL: {name}")
        if message:
            print(f"   Error: {message}")

    results["tests"].append({
        "name": name,
        "passed": passed,
        "message": message
    })

def test_server_health():
    """Test 0: Verify servers are running"""
    try:
        # Backend health
        r = requests.get(f"{BASE_URL}/api/health", timeout=5)
        backend_healthy = r.status_code == 200

        # Frontend health (just check it responds - 404 is OK, means Next.js is running)
        r = requests.get(FRONTEND_URL, timeout=5)
        frontend_healthy = r.status_code in [200, 304, 404]

        passed = backend_healthy and frontend_healthy
        log_test("Server Health Check", passed,
                 f"Backend: {backend_healthy}, Frontend: {frontend_healthy}")
        return passed
    except Exception as e:
        log_test("Server Health Check", False, str(e))
        return False

def test_user_signup(user):
    """Test 1: User signup"""
    try:
        r = requests.post(
            f"{BASE_URL}/api/auth/signup",
            json={
                "name": user["name"],
                "email": user["email"],
                "password": user["password"]
            },
            timeout=10
        )

        passed = r.status_code == 200
        if passed:
            data = r.json()
            # API returns tokens in nested structure
            tokens = data.get("tokens", {})
            user["access_token"] = tokens.get("access_token") or data.get("access_token")
            user["user_id"] = data.get("user", {}).get("id")

        log_test(f"User Signup ({user['email']})", passed,
                 r.text if not passed else "")
        return passed
    except Exception as e:
        log_test(f"User Signup ({user['email']})", False, str(e))
        return False

def test_user_login(user):
    """Test 2: User login"""
    try:
        r = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={
                "email": user["email"],
                "password": user["password"]
            },
            timeout=10
        )

        passed = r.status_code == 200
        if passed:
            data = r.json()
            tokens = data.get("tokens", {})
            user["access_token"] = tokens.get("access_token") or data.get("access_token")

        log_test(f"User Login ({user['email']})", passed,
                 r.text if not passed else "")
        return passed
    except Exception as e:
        log_test(f"User Login ({user['email']})", False, str(e))
        return False

def test_create_task_ui(user):
    """Test 3: Create task via API (simulates UI)"""
    try:
        headers = {"Authorization": f"Bearer {user['access_token']}"}
        r = requests.post(
            f"{BASE_URL}/api/tasks",
            headers=headers,
            json={
                "title": "Test Task via API",
                "description": "Testing task creation",
                "priority": "high"
            },
            timeout=10
        )

        passed = r.status_code == 201
        if passed:
            user["task_id"] = r.json().get("id")

        log_test(f"Create Task - API ({user['email']})", passed,
                 r.text if not passed else "")
        return passed
    except Exception as e:
        log_test(f"Create Task - API ({user['email']})", False, str(e))
        return False

def test_chatbot_create_task(user):
    """Test 4: AI Chatbot - Create task [CRITICAL - Phase III]"""
    try:
        headers = {"Authorization": f"Bearer {user['access_token']}"}

        start_time = time.time()
        r = requests.post(
            f"{BASE_URL}/api/chat",
            headers=headers,
            json={
                "message": "add task buy groceries tomorrow",
                "conversation_id": None
            },
            timeout=15
        )
        response_time = time.time() - start_time

        passed = (
            r.status_code == 200 and
            response_time < 5.0 and
            "groceries" in r.json().get("response", "").lower()
        )

        message = f"Response time: {response_time:.2f}s"
        if response_time >= 5.0:
            message += " (EXCEEDS 5s SLA!)"

        log_test(f"AI Chatbot - Create Task ({user['email']})", passed, message)

        if passed:
            user["chat_conversation_id"] = r.json().get("conversation_id")

        return passed
    except Exception as e:
        log_test(f"AI Chatbot - Create Task ({user['email']})", False, str(e))
        return False

def test_chatbot_list_tasks(user):
    """Test 5: AI Chatbot - List tasks [CRITICAL - Phase III]"""
    try:
        headers = {"Authorization": f"Bearer {user['access_token']}"}

        r = requests.post(
            f"{BASE_URL}/api/chat",
            headers=headers,
            json={
                "message": "show my tasks",
                "conversation_id": user.get("chat_conversation_id")
            },
            timeout=15
        )

        passed = r.status_code == 200

        log_test(f"AI Chatbot - List Tasks ({user['email']})", passed,
                 r.text if not passed else "")
        return passed
    except Exception as e:
        log_test(f"AI Chatbot - List Tasks ({user['email']})", False, str(e))
        return False

def test_chatbot_complete_task(user):
    """Test 6: AI Chatbot - Complete task [CRITICAL - Phase III]"""
    try:
        headers = {"Authorization": f"Bearer {user['access_token']}"}

        r = requests.post(
            f"{BASE_URL}/api/chat",
            headers=headers,
            json={
                "message": "mark task 1 as done",
                "conversation_id": user.get("chat_conversation_id")
            },
            timeout=15
        )

        passed = r.status_code == 200

        log_test(f"AI Chatbot - Complete Task ({user['email']})", passed,
                 r.text if not passed else "")
        return passed
    except Exception as e:
        log_test(f"AI Chatbot - Complete Task ({user['email']})", False, str(e))
        return False

def test_user_isolation():
    """Test 7: User isolation [CRITICAL - Security]"""
    try:
        # User 1 gets their tasks
        headers1 = {"Authorization": f"Bearer {user1['access_token']}"}
        r1 = requests.get(f"{BASE_URL}/api/tasks", headers=headers1, timeout=10)

        # User 2 gets their tasks
        headers2 = {"Authorization": f"Bearer {user2['access_token']}"}
        r2 = requests.get(f"{BASE_URL}/api/tasks", headers=headers2, timeout=10)

        if r1.status_code == 200 and r2.status_code == 200:
            tasks1 = r1.json()
            tasks2 = r2.json()

            # Verify no overlap in task IDs
            ids1 = {t["id"] for t in tasks1}
            ids2 = {t["id"] for t in tasks2}

            passed = len(ids1.intersection(ids2)) == 0
            message = f"User1 tasks: {len(ids1)}, User2 tasks: {len(ids2)}, Overlap: {len(ids1.intersection(ids2))}"
        else:
            passed = False
            message = f"Failed to fetch tasks (Status: {r1.status_code}, {r2.status_code})"

        log_test("User Isolation - Security", passed, message)
        return passed
    except Exception as e:
        log_test("User Isolation - Security", False, str(e))
        return False

def print_summary():
    """Print test summary"""
    print("\n" + "="*60)
    print("CRITICAL E2E TEST RESULTS")
    print("="*60)
    print(f"Total Tests: {results['total']}")
    print(f"Passed: {results['passed']} ✅")
    print(f"Failed: {results['failed']} ❌")
    print(f"Pass Rate: {(results['passed']/results['total']*100):.1f}%")
    print("="*60)

    if results['failed'] > 0:
        print("\nFAILED TESTS:")
        for test in results['tests']:
            if not test['passed']:
                print(f"  - {test['name']}")
                if test['message']:
                    print(f"    {test['message']}")

    print("\nGO/NO-GO DECISION:")
    if results['failed'] == 0:
        print("✅ GO FOR DEPLOYMENT - All critical tests passed")
        return 0
    elif results['failed'] <= 1 and results['passed'] >= 6:
        print("⚠️  CONDITIONAL GO - 1 non-critical failure, review required")
        return 1
    else:
        print("❌ NO-GO - Critical failures detected, fix before deployment")
        return 2

def main():
    """Run all critical tests"""
    print("="*60)
    print("CRITICAL E2E TEST SUITE - AUTOMATED")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    print()

    # Test 0: Server health
    if not test_server_health():
        print("\n❌ ABORT: Servers not running or unhealthy")
        print("Start servers first:")
        print("  Backend: cd backend && uvicorn src.main:app --reload")
        print("  Frontend: cd frontend && npm run dev")
        return 3

    print()

    # Test 1-2: User 1 signup and login
    test_user_signup(user1)
    test_user_login(user1)

    print()

    # Test 3: Create task via API (UI simulation)
    test_create_task_ui(user1)

    print()

    # Test 4-6: AI Chatbot (Phase III Critical)
    print("PHASE III - AI CHATBOT TESTS:")
    test_chatbot_create_task(user1)
    test_chatbot_list_tasks(user1)
    test_chatbot_complete_task(user1)

    print()

    # Test 7: User isolation (create user 2)
    print("SECURITY TEST:")
    test_user_signup(user2)
    test_create_task_ui(user2)
    test_user_isolation()

    # Print summary and return exit code
    return print_summary()

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test suite interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
