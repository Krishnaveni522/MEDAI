"""
Hybrid OCR using EasyOCR (better for difficult images) with Tesseract fallback.
"""

from PIL import Image, ImageEnhance, ImageOps
from io import BytesIO
import time

# Fix for Pillow compatibility - EasyOCR uses deprecated ANTIALIAS
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS
    print("[OCR] Applied Pillow compatibility fix for EasyOCR")

# Try to import easyocr
try:
    import easyocr
    EASYOCR_AVAILABLE = True
    print("[OCR] EasyOCR is available")
except ImportError:
    EASYOCR_AVAILABLE = False
    print("[OCR] EasyOCR not available, will use Tesseract only")

# Tesseract fallback
import pytesseract
pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize EasyOCR reader (only once)
_reader = None

def _get_reader():
    """Lazy load EasyOCR reader"""
    global _reader
    if _reader is None and EASYOCR_AVAILABLE:
        print("[OCR] Initializing EasyOCR reader...")
        _reader = easyocr.Reader(['en'], gpu=False)
        print("[OCR] EasyOCR ready")
    return _reader


def extract_text_from_image(file_storage, time_limit=25.0):
    """
    Extract text using EasyOCR (primary) or Tesseract (fallback).
    EasyOCR is much better at handling rotated and difficult images.
    """
    start_time = time.time()
    
    try:
        # Load image
        print(f"[OCR] Starting OCR process...", flush=True)
        file_storage.seek(0)
        image_bytes = file_storage.read()
        print(f"[OCR] Read {len(image_bytes)} bytes from file", flush=True)
        
        img = Image.open(BytesIO(image_bytes))
        print(f"[OCR] Image opened successfully, format: {img.format}", flush=True)
        
        img = ImageOps.exif_transpose(img).convert("RGB")
        print(f"[OCR] Image size: {img.size[0]}×{img.size[1]}", flush=True)
        
        # Try EasyOCR first if available
        if EASYOCR_AVAILABLE:
            print("[OCR] Trying EasyOCR...", flush=True)
            
            reader = _get_reader()
            if reader:
                # Try different rotations
                w, h = img.size
                if h > w * 1.3:
                    rotations = [90, 270, 0, 180]
                else:
                    rotations = [0, 90, 270, 180]
                
                best_result = None
                best_score = 0
                
                for rotation in rotations:
                    if time.time() - start_time > time_limit:
                        break
                    
                    print(f"[OCR] EasyOCR testing rotation: {rotation}°", flush=True)
                    
                    # Rotate image
                    if rotation != 0:
                        rotated = img.rotate(rotation, expand=True, fillcolor='white')
                    else:
                        rotated = img
                    
                    # Scale if too small
                    w, h = rotated.size
                    if max(w, h) < 1000:
                        scale = 1000 / max(w, h)
                        new_w = int(w * scale)
                        new_h = int(h * scale)
                        rotated = rotated.resize((new_w, new_h), Image.Resampling.LANCZOS)
                    
                    # Convert to RGB numpy array for EasyOCR
                    import numpy as np
                    img_array = np.array(rotated)
                    
                    try:
                        # EasyOCR returns list of (bbox, text, confidence)
                        # Suppress PIL.Image.ANTIALIAS warnings/errors
                        import warnings
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore")
                            results = reader.readtext(img_array, detail=1)
                        
                        if results:
                            # Combine all detected text
                            texts = [text for (bbox, text, conf) in results if conf > 0.3]
                            combined_text = ' '.join(texts)
                            
                            if combined_text.strip():
                                # Calculate quality score based on text readability
                                letters = sum(1 for c in combined_text if c.isalpha())
                                digits = sum(1 for c in combined_text if c.isdigit())
                                avg_conf = sum(conf for (bbox, text, conf) in results) / len(results)
                                
                                # Base score from confidence and character counts
                                score = letters * 2.0 + digits * 1.5 + avg_conf * 100
                                
                                # Check for readable words (indication of correct orientation)
                                text_lower = combined_text.lower()
                                words = text_lower.split()
                                
                                # Common medicine-related words
                                med_keywords = ['cream', 'gel', 'ointment', 'lotion', 'tablet', 'capsule',
                                              'mg', 'ml', 'gm', 'syrup', 'solution', 'suspension',
                                              'tacrolimus', 'aspirin', 'paracetamol', 'ibuprofen',
                                              'apply', 'take', 'oral', 'topical', 'external', 'use',
                                              'healthcare', 'pharma', 'laboratory', 'drug']
                                
                                # Bonus points for medicine keywords (strong indicator of correct orientation)
                                keyword_matches = sum(100 for kw in med_keywords if kw in text_lower)
                                score += keyword_matches
                                
                                # Check for proper word structure (vowels present, reasonable length)
                                valid_words = 0
                                for word in words:
                                    if len(word) >= 3:
                                        # Check if word has vowels (readable text usually does)
                                        has_vowels = any(v in word for v in 'aeiou')
                                        # Check reasonable consonant-vowel ratio
                                        vowel_count = sum(1 for c in word if c in 'aeiou')
                                        consonant_count = sum(1 for c in word if c.isalpha() and c not in 'aeiou')
                                        
                                        if has_vowels and vowel_count > 0 and consonant_count > 0:
                                            ratio = consonant_count / vowel_count
                                            if 0.5 <= ratio <= 4.0:  # Reasonable ratio for English
                                                valid_words += 1
                                
                                # Add bonus for valid word structure
                                score += valid_words * 30
                                
                                # Penalty for excessive special characters (garbled text indicator)
                                special_chars = sum(1 for c in combined_text if not c.isalnum() and c not in ' .,-%/')
                                if special_chars > len(combined_text) * 0.3:
                                    score *= 0.5  # Heavy penalty for garbled text
                                
                                print(f"  EasyOCR found: {len(results)} regions, {valid_words} valid words, score={score:.1f}", flush=True)
                                print(f"  Text preview: {combined_text[:100]}", flush=True)
                                
                                if score > best_score:
                                    best_score = score
                                    best_result = {
                                        'text': combined_text,
                                        'rotation': rotation,
                                        'score': score,
                                        'confidence': avg_conf
                                    }
                    
                    except Exception as e:
                        print(f"  EasyOCR error at {rotation}°: {e}", flush=True)
                        continue
                
                # Return best EasyOCR result
                if best_result and best_result['score'] > 10:
                    print(f"\n[OCR] ✓ EasyOCR SUCCESS!", flush=True)
                    print(f"  Rotation: {best_result['rotation']}°", flush=True)
                    print(f"  Score: {best_result['score']:.1f}", flush=True)
                    print(f"  Confidence: {best_result['confidence']:.2f}", flush=True)
                    return best_result['text']
        
        # Fallback to Tesseract
        print("[OCR] Falling back to Tesseract...", flush=True)
        return _tesseract_ocr(img, time_limit - (time.time() - start_time))
    
    except Exception as e:
        print(f"[OCR] Error: {e}", flush=True)
        return f"Error processing image: {str(e)}"


def _tesseract_ocr(img, time_remaining):
    """Tesseract OCR fallback with improved preprocessing"""
    start_time = time.time()
    
    w, h = img.size
    if h > w * 1.3:
        rotations = [90, 270, 0, 180]
    else:
        rotations = [0, 90, 270, 180]
    
    best_text = ""
    best_letters = 0
    
    for rotation in rotations:
        if time.time() - start_time > time_remaining:
            break
        
        print(f"[OCR] Tesseract testing rotation: {rotation}°", flush=True)
        
        if rotation != 0:
            rotated = img.rotate(rotation, expand=True, fillcolor='white')
        else:
            rotated = img
        
        # Scale to optimal size for Tesseract
        w, h = rotated.size
        if max(w, h) < 2000:
            scale = 2000 / max(w, h)
            new_w = int(w * scale)
            new_h = int(h * scale)
            scaled = rotated.resize((new_w, new_h), Image.Resampling.LANCZOS)
        else:
            scaled = rotated
        
        # Try multiple preprocessing variants
        variants = []
        
        # Original scaled
        variants.append(('original', scaled))
        
        # Grayscale with contrast enhancement
        gray = scaled.convert('L')
        variants.append(('gray', gray))
        
        # High contrast
        enhancer = ImageEnhance.Contrast(gray)
        high_contrast = enhancer.enhance(2.5)
        variants.append(('high_contrast', high_contrast))
        
        # Sharpness enhancement
        sharpener = ImageEnhance.Sharpness(gray)
        sharpened = sharpener.enhance(2.0)
        variants.append(('sharpened', sharpened))
        
        for variant_name, variant in variants:
            try:
                # Try different PSM modes
                configs = [
                    '--oem 3 --psm 6',  # Assume uniform block of text
                    '--oem 3 --psm 11', # Sparse text
                    '--oem 3 --psm 3',  # Fully automatic
                ]
                
                for config in configs:
                    text = pytesseract.image_to_string(variant, config=config)
                    text = text.strip()
                    
                    if text:
                        letters = sum(1 for c in text if c.isalpha())
                        
                        # Quality check - count valid words
                        text_lower = text.lower()
                        words = [w for w in text_lower.split() if len(w) >= 3]
                        valid_words = 0
                        
                        for word in words:
                            has_vowels = any(v in word for v in 'aeiou')
                            if has_vowels:
                                vowel_count = sum(1 for c in word if c in 'aeiou')
                                consonant_count = sum(1 for c in word if c.isalpha() and c not in 'aeiou')
                                if vowel_count > 0 and consonant_count > 0:
                                    ratio = consonant_count / vowel_count
                                    if 0.5 <= ratio <= 4.0:
                                        valid_words += 1
                        
                        # Check for medicine keywords
                        med_keywords = ['cream', 'gel', 'ointment', 'tablet', 'mg', 'ml', 'tacrolimus']
                        has_keywords = any(kw in text_lower for kw in med_keywords)
                        
                        # Calculate quality score
                        quality_score = letters + (valid_words * 10) + (50 if has_keywords else 0)
                        
                        if quality_score > best_letters:
                            best_letters = quality_score
                            best_text = text
                            print(f"  Tesseract found: {letters} letters, {valid_words} valid words, score={quality_score} ({variant_name})", flush=True)
                            print(f"  Preview: {text[:100]}", flush=True)
            except Exception as e:
                print(f"  Tesseract error with {variant_name}: {e}", flush=True)
                continue
    
    if best_text and best_letters > 3:
        print(f"[OCR] ✓ Tesseract SUCCESS: {best_letters} letters", flush=True)
        return best_text
    
    print(f"[OCR] ✗ Tesseract FAILED: Could not extract readable text", flush=True)
    return "Could not extract readable text from image"
