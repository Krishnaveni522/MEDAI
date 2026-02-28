"""
Test script to verify Tacrolimus matching with the uploaded image
"""
import sys
sys.path.insert(0, r'c:\Users\Asus\Downloads\kvfinaloutput\medai\src')

from utils.database import get_all_drugs_dict, add_drug
from app import match_instructions

# First, ensure Tacrolimus is in the database
print("Step 1: Checking database for Tacrolimus...")
drugs = get_all_drugs_dict()

if 'Tacrolimus' not in drugs and 'Tacrolimus Ointment' not in drugs:
    print("Adding Tacrolimus Ointment to database...")
    add_drug(
        'Tacrolimus Ointment',
        'Tacrolimus 0.03% ointment is used to treat eczema (atopic dermatitis). Apply a thin layer to affected areas twice daily. Wash hands before and after application. Avoid contact with eyes. For external use only. Continue treatment as prescribed by doctor.'
    )
    print("✓ Tacrolimus Ointment added to database")
else:
    print("✓ Tacrolimus already in database")

# Test with sample OCR text from the image
print("\nStep 2: Testing OCR text matching...")
sample_ocr_texts = [
    "Tacrolimus Ointment 0.03% w/w",
    "Tacrolimus 0.03",
    "prevego Tacrolimus Ointment 0.03% w/w 10g",
    "tacrolimus ointment",
]

for ocr_text in sample_ocr_texts:
    print(f"\n--- Testing OCR: '{ocr_text}' ---")
    matches = match_instructions(ocr_text, cutoff=0.25, max_results=5)
    
    if matches:
        print(f"✓ Found {len(matches)} match(es):")
        for drug_name, matched_variant, snippet, score in matches:
            print(f"  - Drug: {drug_name}")
            print(f"    Variant: {matched_variant}")
            print(f"    Score: {score * 100:.1f}%")
            print(f"    Instructions: {snippet[:100]}...")
    else:
        print("✗ No matches found")

print("\n" + "="*60)
print("Test completed!")
