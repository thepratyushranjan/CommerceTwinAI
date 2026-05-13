import sys
import os
import json

# Add project root to path
sys.path.append(os.getcwd())

from modules.support.agent import run_agent

def test_support_agent():
    print("🚀 Starting Customer Support Agent End-to-End Test...")
    
    test_queries = [
        "Where is my order ORD-1005?",
        "What is your return policy?",
        "I want to return ORD-1002, what is the procedure?",
        "I need to speak with a human agent immediately.",
        "How do I change my account password?"
    ]
    
    for i, query in enumerate(test_queries):
        print(f"\n--- Test {i+1}: {query} ---")
        try:
            result = run_agent(query, history=[])
            print(f"🤖 Response: {result['response']}")
            
            if result['trace']:
                print(f"🛠️ Tools Used:")
                for step in result['trace']:
                    print(f"  - {step['tool']}")
            else:
                print("⚠️ No tools used.")
                
        except Exception as e:
            print(f"❌ Error in Test {i+1}: {e}")

if __name__ == "__main__":
    test_support_agent()
