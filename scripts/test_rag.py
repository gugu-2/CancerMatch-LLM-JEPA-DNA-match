import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_engine.llm.rag_pipeline import RAGPipeline

def run_test():
    print("Initializing RAG Pipeline...")
    rag = RAGPipeline()
    
    print("\n--- Test 1: Canine Sample ---")
    canine_report = rag.generate_report(species="canine", notes="Suspected septic peritonitis")
    print(json.dumps(canine_report, indent=2))
    
    print("\n--- Test 2: Bovine Sample ---")
    bovine_report = rag.generate_report(species="bovine", notes="Severe respiratory distress")
    print(json.dumps(bovine_report, indent=2))
    
    print("\nTests completed successfully.")

if __name__ == "__main__":
    run_test()
