import pytest
import requests
from typing import Dict, List

API_URL = "http://localhost:8000"

@pytest.fixture
def test_questions():
    """Load test questions"""
    return [
        {"q": "What is the main topic?", "expected": ["topic"]},
        # Add 50 questions here
    ]

def test_accuracy(test_questions):
    """Test accuracy is >= 84%"""
    correct = 0
    
    for item in test_questions[:10]:  # Test first 10
        response = requests.post(
            f"{API_URL}/chat",
            json={"query": item["q"], "session_id": "test"}
        )
        data = response.json()
        
        if any(kw in data["answer"].lower() for kw in item["expected"]):
            correct += 1
    
    accuracy = correct / len(test_questions[:10]) * 100
    assert accuracy >= 84, f"Accuracy {accuracy}% < 84%"

def test_latency(test_questions):
    """Test p95 latency < 320ms"""
    latencies = []
    
    for item in test_questions[:5]:
        response = requests.post(
            f"{API_URL}/chat",
            json={"query": item["q"], "session_id": "test"}
        )
        data = response.json()
        latencies.append(data["latency_ms"])
    
    p95 = sorted(latencies)[int(len(latencies) * 0.95)]
    assert p95 < 320, f"p95 latency {p95}ms > 320ms"

def test_cache_working():
    """Test Redis cache is working"""
    query = "test cache"
    
    # First request
    response1 = requests.post(
        f"{API_URL}/chat",
        json={"query": query, "session_id": "cache_test"}
    )
    data1 = response1.json()
    
    # Second request (should be cached)
    response2 = requests.post(
        f"{API_URL}/chat",
        json={"query": query, "session_id": "cache_test"}
    )
    data2 = response2.json()
    
    assert data2.get("cached", False), "Cache not working"