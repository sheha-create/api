#!/usr/bin/env python
"""
Test script for AI Voice Detector API
Tests health endpoint and basic API functionality
"""

import requests
import json
import sys
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:8000"
API_KEY = "your-default-api-key-change-in-production"

def test_health():
    """Test health endpoint."""
    print("\n" + "="*60)
    print("TEST 1: Health Check")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ PASSED: Health check successful")
            return True
        else:
            print("❌ FAILED: Unexpected status code")
            return False
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False


def test_missing_api_key():
    """Test missing API key."""
    print("\n" + "="*60)
    print("TEST 2: Missing API Key (Should Fail)")
    print("="*60)
    
    try:
        response = requests.post(f"{BASE_URL}/detect-voice")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 401:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            print("✅ PASSED: Correctly rejected missing API key")
            return True
        else:
            print("❌ FAILED: Should return 401 for missing API key")
            return False
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False


def test_invalid_api_key():
    """Test invalid API key."""
    print("\n" + "="*60)
    print("TEST 3: Invalid API Key (Should Fail)")
    print("="*60)
    
    try:
        headers = {"X-API-Key": "invalid-key"}
        response = requests.post(f"{BASE_URL}/detect-voice", headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 403:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            print("✅ PASSED: Correctly rejected invalid API key")
            return True
        else:
            print("❌ FAILED: Should return 403 for invalid API key")
            return False
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False


def test_empty_file():
    """Test empty file submission."""
    print("\n" + "="*60)
    print("TEST 4: Empty File (Should Fail)")
    print("="*60)
    
    try:
        headers = {"X-API-Key": API_KEY}
        files = {'file': ('empty.wav', b'')}
        response = requests.post(
            f"{BASE_URL}/detect-voice",
            headers=headers,
            files=files
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 400:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            print("✅ PASSED: Correctly rejected empty file")
            return True
        else:
            print("❌ FAILED: Should return 400 for empty file")
            return False
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False


def test_invalid_format():
    """Test invalid file format."""
    print("\n" + "="*60)
    print("TEST 5: Invalid File Format (Should Fail)")
    print("="*60)
    
    try:
        headers = {"X-API-Key": API_KEY}
        files = {'file': ('test.txt', b'This is not audio')}
        response = requests.post(
            f"{BASE_URL}/detect-voice",
            headers=headers,
            files=files
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 400:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            print("✅ PASSED: Correctly rejected invalid format")
            return True
        else:
            print("❌ FAILED: Should return 400 for invalid format")
            return False
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False


def run_all_tests():
    """Run all tests."""
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█" + "  AI Voice Detector API - Test Suite".center(58) + "█")
    print("█" + " "*58 + "█")
    print("█"*60)
    
    print(f"\nBase URL: {BASE_URL}")
    print(f"API Key: {API_KEY}")
    
    results = []
    
    # Run tests
    results.append(("Health Check", test_health()))
    results.append(("Missing API Key", test_missing_api_key()))
    results.append(("Invalid API Key", test_invalid_api_key()))
    results.append(("Empty File", test_empty_file()))
    results.append(("Invalid Format", test_invalid_format()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("="*60)
    print(f"Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
