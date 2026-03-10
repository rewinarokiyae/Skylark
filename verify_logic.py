from agent.agent import BIAgent
import pandas as pd

def test_agent_fallback():
    print("Initializing Agent...")
    agent = BIAgent()
    
    print("Testing Query: 'What is the average masked deal value across all deals?'")
    try:
        result = agent.process_query("What is the average masked deal value across all deals?")
        import json
        with open('test_output.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, default=str)
        print("Success: Result saved to test_output.json")
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_agent_fallback()
