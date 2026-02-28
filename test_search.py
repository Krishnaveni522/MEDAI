"""
Quick test of the text search functionality
"""
import sys
sys.path.insert(0, r'c:\Users\Asus\Downloads\kvfinaloutput\medai\src')

from app import match_instructions
from utils.database import get_all_drugs_dict

print("Testing Text Search Functionality")
print("="*60)

# Show available medicines
drugs = get_all_drugs_dict()
print(f"\nTotal medicines in database: {len(drugs)}")
print("\nSample medicines:")
for i, drug in enumerate(list(drugs.keys())[:5], 1):
    print(f"  {i}. {drug}")

# Test searches
test_queries = [
    "Tacrolimus",
    "aspirin",
    "paracetamol",
    "ointment",
    "tac"
]

print("\n" + "="*60)
print("Testing Search Queries:")
print("="*60)

for query in test_queries:
    print(f"\nQuery: '{query}'")
    matches = match_instructions(query, cutoff=0.25, max_results=5)
    
    if matches:
        print(f"✓ Found {len(matches)} match(es):")
        for drug_name, variant, snippet, score in matches:
            print(f"  • {drug_name} (Score: {score*100:.1f}%)")
    else:
        print("  ✗ No matches found")

print("\n" + "="*60)
print("Text search is ready to use!")
print("Access the app at: http://localhost:5000/patient")
