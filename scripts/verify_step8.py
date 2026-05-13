import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from modules.support.agent import run_agent

def verify_step_8():
    print("🧪 Verifying Step 8 Test Conversations...")
    
    test_cases = [
        {"name": "Order Status", "query": "Where is my order ORD-1003?", "expected": "get_order_status"},
        {"name": "Policy Query", "query": "How do I return something?", "expected": "search_knowledge_base"},
        {"name": "Multi-Tool Query", "query": "I want to return ORD-1003, what's your policy?", "expected": ["get_order_status", "search_knowledge_base"]},
        {"name": "Out of Scope", "query": "What's the weather today?", "expected": None},
        {"name": "Explicit Escalation", "query": "I want to speak to a human", "expected": "escalate_to_human"},
        {"name": "Implicit Escalation (Threat)", "query": "I'm going to sue you, my package never arrived!", "expected": "escalate_to_human"},
    ]

    for case in test_cases:
        print(f"\n[Case: {case['name']}]")
        print(f"User: {case['query']}")
        result = run_agent(case['query'], history=[])
        print(f"Agent: {result['response']}")
        
        tools_used = [t['tool'] for t in result['trace']]
        print(f"Tools used: {tools_used}")
        
        # Simple verification logic
        if case['expected'] is None:
            if not tools_used:
                print("✅ Correct: No tools called for out-of-scope query.")
            else:
                print("❌ Failure: Tool called for out-of-scope query.")
        elif isinstance(case['expected'], list):
            missing = [t for t in case['expected'] if t not in tools_used]
            if not missing:
                print(f"✅ Correct: All expected tools called {case['expected']}.")
            else:
                print(f"❌ Failure: Missing tools {missing}.")
        else:
            if case['expected'] in tools_used:
                print(f"✅ Correct: Tool {case['expected']} called.")
            else:
                print(f"❌ Failure: Tool {case['expected']} NOT called.")

    # Multi-turn test
    print("\n[Case: Multi-turn Memory]")
    print("User: I have an issue")
    res1 = run_agent("I have an issue", history=[])
    print(f"Agent: {res1['response']}")
    
    # Simulate history
    history = [("user", "I have an issue"), ("assistant", res1['response'])]
    print("User: It's about ORD-1005")
    res2 = run_agent("It's about ORD-1005", history=history)
    print(f"Agent: {res2['response']}")
    
    if "get_order_status" in [t['tool'] for t in res2['trace']]:
        print("✅ Correct: Agent remembered context and looked up ORD-1005.")
    else:
        print("❌ Failure: Agent failed to link ORD-1005 to the 'issue' in history.")

    # Email search test
    print("\n[Case: Email Search Adaptation]")
    print("User: Show me orders for alice@example.com")
    res_email = run_agent("Show me orders for alice@example.com", history=[])
    print(f"Agent: {res_email['response']}")
    print(f"Tools used: {[t['tool'] for t in res_email['trace']]}")

if __name__ == "__main__":
    verify_step_8()
