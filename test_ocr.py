"""
Test OCR with a sample image
"""
import sys
sys.path.insert(0, r'c:\Users\Asus\Downloads\kvfinaloutput\medai\src')

from utils.ocr_easyocr import extract_text_from_image
from io import BytesIO

print("Testing OCR Functionality")
print("="*60)

# Check if there's a test image
import os

test_images = [
    r"C:\Users\Asus\Downloads\kvfinaloutput\medai\src\uploads",
    r"C:\Users\Asus\Downloads\kvfinaloutput\medai\src",
]

print("\nLooking for test images...")
for folder in test_images:
    if os.path.exists(folder):
        print(f"\nChecking: {folder}")
        files = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if files:
            print(f"Found {len(files)} image(s):")
            for f in files[:3]:
                print(f"  • {f}")
                
                # Test OCR on first image
                filepath = os.path.join(folder, f)
                print(f"\n  Testing OCR on: {f}")
                
                try:
                    with open(filepath, 'rb') as img_file:
                        # Create a file-like object that simulates Flask's FileStorage
                        class FileStorage:
                            def __init__(self, file_content):
                                self.content = file_content
                                self.position = 0
                            
                            def read(self):
                                return self.content
                            
                            def seek(self, position):
                                self.position = position
                        
                        file_content = img_file.read()
                        file_obj = FileStorage(file_content)
                        
                        result = extract_text_from_image(file_obj)
                        print(f"\n  OCR Result ({len(result)} chars):")
                        print(f"  {result[:200]}")
                        
                except Exception as e:
                    print(f"  Error: {e}")
                
                break  # Only test first image
            break

print("\n" + "="*60)
print("If no images found, please upload via the web interface")
