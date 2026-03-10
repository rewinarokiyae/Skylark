from agent.agent import BIAgent
import pandas as pd

def test_agent_fallback():
    print("Initializing Agent...")
    agent = BIAgent()
    
    print("Testing Query: 'How is our pipeline looking for the mining sector?'")
    try:
        # This will attempt API call, fail (likely), and fallback to CSV
        result = agent.process_query("How is our pipeline looking for the mining sector?")
        print("\n--- INTENT ---")
        print(result['intent'])
        print("\n--- METRIC ---")
        print(result['metric_data'])
        print("\n--- INSIGHT ---")
        print(result['insight'])
        
        if result['quality_issues']:
            print("\n--- QUALITY ISSUES ---")
            for issue in result['quality_issues']:
                print(f"- {issue}")
                
    except Exception as e:
        print(f"Test failed with error: {e}")

if __name__ == "__main__":
    test_agent_fallback()
