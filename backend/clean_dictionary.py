#!/usr/bin/env python3
"""
Script to clean up and refine the extracted dictionary entries.
"""

import json
import re
from pathlib import Path

def clean_ijaw_translation(text):
    """Clean up Ijaw translation text."""
    if not text:
        return ""
    
    # Remove common PDF artifacts and formatting
    text = re.sub(r'[¢]+', '', text)  # Remove ¢ symbols
    text = re.sub(r'[!!!]+', '!', text)  # Normalize exclamation marks
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    text = re.sub(r'^\s*[A-Z]\.\s*', '', text)  # Remove leading "A. " or "B. " etc.
    text = re.sub(r'\([^)]*\)', '', text)  # Remove parenthetical content
    text = re.sub(r'\[[^\]]*\]', '', text)  # Remove bracketed content
    text = re.sub(r'[;:]\s*$', '', text)  # Remove trailing semicolons/colons
    text = text.strip()
    
    # If text is too long or contains too many English words, it's probably not a clean translation
    if len(text) > 50 or len([w for w in text.split() if re.match(r'^[a-zA-Z]+$', w)]) > 3:
        return ""
    
    return text

def clean_english_word(word):
    """Clean up English word."""
    if not word:
        return ""
    
    word = word.strip().lower()
    word = re.sub(r'[^\w\s]', '', word)  # Remove punctuation
    word = re.sub(r'\s+', ' ', word)  # Normalize whitespace
    
    # Skip if too long or contains numbers
    if len(word) > 30 or re.search(r'\d', word):
        return ""
    
    # Skip if it looks like a phrase fragment
    if word.startswith(('a ', 'an ', 'the ', 'of ', 'in ', 'on ', 'at ', 'to ', 'for ', 'with ', 'by ')):
        return ""
    
    return word

def is_valid_entry(english, ijaw):
    """Check if a dictionary entry is valid."""
    if not english or not ijaw:
        return False
    
    # English should be reasonable length
    if len(english) < 2 or len(english) > 25:
        return False
    
    # Ijaw should be reasonable length
    if len(ijaw) < 1 or len(ijaw) > 30:
        return False
    
    # English should not contain too many non-alphabetic characters
    if len(re.sub(r'[a-zA-Z\s]', '', english)) > 2:
        return False
    
    # Skip entries that are clearly fragments or artifacts
    skip_patterns = [
        r'^\d+',  # Starts with number
        r'page \d+',  # Page references
        r'fig\.',  # Figure references
        r'cf\.',  # Cross references
        r'lit\.',  # Literal translations
        r'i\.e\.',  # That is
        r'etc\.',  # Et cetera
    ]
    
    for pattern in skip_patterns:
        if re.search(pattern, english, re.IGNORECASE):
            return False
    
    return True

def load_and_clean_dictionary():
    """Load and clean the dictionary."""
    json_path = Path("dictionaries/en_to_ijaw.json")
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            raw_dict = json.load(f)
    except Exception as e:
        print(f"Error loading dictionary: {e}")
        return {}
    
    print(f"Loaded {len(raw_dict)} raw entries")
    
    cleaned_dict = {}
    
    for english, ijaw in raw_dict.items():
        # Clean both parts
        clean_eng = clean_english_word(english)
        clean_ijaw = clean_ijaw_translation(ijaw)
        
        # Validate entry
        if is_valid_entry(clean_eng, clean_ijaw):
            cleaned_dict[clean_eng] = clean_ijaw
    
    print(f"Cleaned dictionary has {len(cleaned_dict)} valid entries")
    print(f"Removed {len(raw_dict) - len(cleaned_dict)} invalid entries")
    
    return cleaned_dict

def add_common_words():
    """Add some common words that might be missing."""
    common_words = {
        # Basic greetings and responses
        "hello": "Dó!",
        "hi": "Dó!",
        "goodbye": "Egiri kéinkein yò!",
        "bye": "Egiri kéinkein yò!",
        "thank you": "Nụ́ à",
        "thanks": "Nụ́ à",
        "please": "Biko",
        "yes": "Ịyaa",
        "no": "Áàị́n",
        
        # Family
        "father": "papa",
        "mother": "mama",
        "brother": "bara",
        "sister": "sista",
        "child": "omo",
        "family": "wárịbịbị̀",
        
        # Basic needs
        "water": "bení",
        "food": "fị́yaị",
        "house": "wárị",
        "money": "kudi",
        
        # Actions
        "come": "bia",
        "go": "gha",
        "eat": "yei",
        "drink": "mu",
        "sleep": "turu",
        "work": "wok",
        
        # Time
        "time": "taim",
        "day": "dei",
        "night": "nait",
        "morning": "mornin",
        "today": "tude",
        "tomorrow": "tumoro",
        "yesterday": "yestade",
        
        # Descriptors
        "good": "botu",
        "bad": "kiri",
        "big": "toru",
        "small": "kiri-kiri",
        "beautiful": "fain",
        
        # People
        "man": "okpo",
        "woman": "teme",
        "friend": "padi",
        
        # Emotions/concepts
        "love": "yenagha",
        "peace": "fred",
        "happy": "hapi",
        "sad": "sad",
    }
    
    return common_words

def main():
    # Clean the existing dictionary
    cleaned_dict = load_and_clean_dictionary()
    
    # Add common words (existing entries take precedence)
    common_words = add_common_words()
    final_dict = {**common_words, **cleaned_dict}
    
    print(f"Final dictionary has {len(final_dict)} entries")
    
    # Save cleaned dictionary
    json_path = Path("dictionaries/en_to_ijaw.json")
    try:
        # Sort dictionary by keys
        sorted_dict = dict(sorted(final_dict.items()))
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(sorted_dict, f, ensure_ascii=False, indent=2)
        
        print(f"Cleaned dictionary saved to {json_path}")
        
        # Show some sample entries
        print("\nSample entries:")
        for i, (eng, ijaw) in enumerate(list(sorted_dict.items())[:15]):
            print(f"  {eng}: {ijaw}")
        
        return True
    except Exception as e:
        print(f"Error saving dictionary: {e}")
        return False

if __name__ == "__main__":
    main()