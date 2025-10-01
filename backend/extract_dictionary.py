#!/usr/bin/env python3
"""
Script to extract English-Ijaw dictionary entries from the Izon dictionary PDF
and generate/update the en_to_ijaw.json file.
"""

import pdfplumber
import json
import re
import os
from pathlib import Path

def extract_dictionary_from_pdf(pdf_path):
    """Extract dictionary entries from the PDF file."""
    dictionary = {}
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"Processing PDF with {len(pdf.pages)} pages...")
            
            for page_num, page in enumerate(pdf.pages, 1):
                print(f"Processing page {page_num}...")
                text = page.extract_text()
                
                if text:
                    # Look for dictionary entries in various formats
                    # Common patterns: "English word - Ijaw translation"
                    # or "English word: Ijaw translation"
                    # or "English word = Ijaw translation"
                    
                    lines = text.split('\n')
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                            
                        # Pattern 1: word - translation
                        match = re.match(r'^([a-zA-Z\s]+)\s*[-–—]\s*([^\s].*?)(?:\s*\([^)]*\))?$', line)
                        if match:
                            english = match.group(1).strip().lower()
                            ijaw = match.group(2).strip()
                            if english and ijaw and len(english.split()) <= 3:  # Avoid long phrases
                                dictionary[english] = ijaw
                                continue
                        
                        # Pattern 2: word : translation
                        match = re.match(r'^([a-zA-Z\s]+)\s*:\s*([^\s].*?)(?:\s*\([^)]*\))?$', line)
                        if match:
                            english = match.group(1).strip().lower()
                            ijaw = match.group(2).strip()
                            if english and ijaw and len(english.split()) <= 3:
                                dictionary[english] = ijaw
                                continue
                        
                        # Pattern 3: word = translation
                        match = re.match(r'^([a-zA-Z\s]+)\s*=\s*([^\s].*?)(?:\s*\([^)]*\))?$', line)
                        if match:
                            english = match.group(1).strip().lower()
                            ijaw = match.group(2).strip()
                            if english and ijaw and len(english.split()) <= 3:
                                dictionary[english] = ijaw
                                continue
                        
                        # Pattern 4: Look for lines with both English and non-English words
                        # This is more flexible but might catch false positives
                        words = line.split()
                        if len(words) >= 2:
                            # Check if line contains both English-like and non-English-like words
                            english_words = []
                            ijaw_words = []
                            
                            for word in words:
                                word = re.sub(r'[^\w\s]', '', word).strip()
                                if word and word.isalpha():
                                    # Simple heuristic: if word contains only common English letters
                                    if re.match(r'^[a-zA-Z]+$', word) and len(word) > 1:
                                        english_words.append(word.lower())
                                    else:
                                        ijaw_words.append(word)
                            
                            if len(english_words) == 1 and len(ijaw_words) >= 1:
                                english = english_words[0]
                                ijaw = ' '.join(ijaw_words)
                                if len(english) > 1 and len(ijaw) > 1:
                                    dictionary[english] = ijaw
    
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return {}
    
    return dictionary

def load_existing_dictionary(json_path):
    """Load existing dictionary from JSON file."""
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading existing dictionary: {e}")
            return {}
    return {}

def save_dictionary(dictionary, json_path):
    """Save dictionary to JSON file."""
    try:
        # Sort dictionary by keys for better organization
        sorted_dict = dict(sorted(dictionary.items()))
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(sorted_dict, f, ensure_ascii=False, indent=2)
        
        print(f"Dictionary saved to {json_path}")
        print(f"Total entries: {len(sorted_dict)}")
        return True
    except Exception as e:
        print(f"Error saving dictionary: {e}")
        return False

def main():
    # Paths
    pdf_path = Path("../Izon dictionary.pdf")
    json_path = Path("dictionaries/en_to_ijaw.json")
    
    print("Extracting dictionary from PDF...")
    
    # Check if PDF exists
    if not pdf_path.exists():
        print(f"PDF file not found: {pdf_path}")
        return
    
    # Extract from PDF
    extracted_dict = extract_dictionary_from_pdf(pdf_path)
    print(f"Extracted {len(extracted_dict)} entries from PDF")
    
    # Load existing dictionary
    existing_dict = load_existing_dictionary(json_path)
    print(f"Loaded {len(existing_dict)} existing entries")
    
    # Merge dictionaries (existing entries take precedence)
    merged_dict = {**extracted_dict, **existing_dict}
    
    print(f"Merged dictionary has {len(merged_dict)} total entries")
    print(f"New entries added: {len(merged_dict) - len(existing_dict)}")
    
    # Save merged dictionary
    if save_dictionary(merged_dict, json_path):
        print("Dictionary update completed successfully!")
        
        # Show some sample new entries
        new_entries = {k: v for k, v in extracted_dict.items() if k not in existing_dict}
        if new_entries:
            print("\nSample new entries:")
            for i, (eng, ijaw) in enumerate(list(new_entries.items())[:10]):
                print(f"  {eng}: {ijaw}")
            if len(new_entries) > 10:
                print(f"  ... and {len(new_entries) - 10} more")
    else:
        print("Failed to save dictionary")

if __name__ == "__main__":
    main()