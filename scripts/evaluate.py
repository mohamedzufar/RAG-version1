#!/usr/bin/env python
"""
Evaluate accuracy on 50 questions
Target: 84% accuracy
"""
import requests
import json
import time
from typing import List, Dict

API_URL = "http://localhost:8000"

# Add your test questions here
# Format: {"q": "question", "expected": ["keyword1", "keyword2"]}
TEST_QUESTIONS = [
    # Example questions - replace with your own
    {"q": "What is the main topic of this document?", "expected": ["topic", "main"]},
    {"q": "Who is the author?", "expected": ["author", "written by"]},
    {"q": "What is the main argument?", "expected": ["argument", "argues"]},
    # Add 47 more questions here...
]

def evaluate_accuracy(test_questions: List[Dict]) -> Dict:
    results = []
    correct = 0
    
    print(f"🔄 Evaluating {len(test_questions)} questions...")
    print("-" * 50)
    
    for i, item in enumerate(test_questions):
        question = item["q"]
        expected_keywords = item["expected"]
        
        try:
            response = requests.post(
                f"{API_URL}/chat",
                json={
                    "query": question,
                    "session_id": "evaluation",
                    "include_sources": True
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                answer = data["answer"].lower()
                confidence = data["confidence"]
                
                # Check keywords
                is_correct = any(
                    keyword.lower() in answer 
                    for keyword in expected_keywords
                )
                
                if is_correct:
                    correct += 1
                    status = "✅"
                else:
                    status = "❌"
                
                results.append({
                    "question": question,
                    "answer": answer[:100],
                    "expected": expected_keywords,
                    "is_correct": is_correct,
                    "confidence": confidence,
                    "status": status
                })
                
                print(f"{status} Q{i+1}: {question[:50]}...")
                print(f"   Answer: {answer[:100]}...")
                print(f"   Expected: {', '.join(expected_keywords)}")
                print(f"   Confidence: {confidence:.2f}")
                print("-" * 30)
                
            else:
                print(f"⚠️ Error on question {i+1}: {response.text}")
        
        except Exception as e:
            print(f"❌ Error on question {i+1}: {str(e)}")
        
        time.sleep(0.1)  # Rate limiting
    
    # Calculate results
    accuracy = (correct / len(test_questions)) * 100
    
    print("\n" + "=" * 50)
    print("📊 EVALUATION RESULTS")
    print("=" * 50)
    print(f"Total Questions: {len(test_questions)}")
    print(f"Correct: {correct}")
    print(f"Incorrect: {len(test_questions) - correct}")
    print(f"✅ Accuracy: {accuracy:.2f}%")
    print(f"🎯 Target: 84%")
    
    if accuracy >= 84:
        print("🎉 PASSED!")
    else:
        print(f"⚠️ Need {84 - accuracy:.2f}% improvement")
    
    return {
        "accuracy": accuracy,
        "total": len(test_questions),
        "correct": correct,
        "incorrect": len(test_questions) - correct,
        "results": results
    }

if __name__ == "__main__":
    print("🚀 Starting Accuracy Evaluation")
    print(f"Target: 84% accuracy")
    print(f"API: {API_URL}")
    print("=" * 50)
    
    # Run evaluation
    results = evaluate_accuracy(TEST_QUESTIONS)
    
    # Save results
    with open("evaluation_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📁 Results saved to evaluation_results.json")