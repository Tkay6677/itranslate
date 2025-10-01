#!/usr/bin/env python3
"""
Script to organize the English to Ijaw dictionary into logical categories
and alphabetical order for better readability and maintenance.
"""

import json
import re
from collections import OrderedDict

def load_dictionary(file_path):
    """Load the dictionary from JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def categorize_entries(dictionary):
    """Categorize dictionary entries into logical groups"""
    categories = {
        'greetings_and_politeness': {},
        'basic_words': {},
        'common_phrases': {},
        'complete_sentences': {}
    }
    
    # Define greeting and politeness patterns
    greetings = [
        'hello', 'goodbye', 'thank you', 'please', 'yes', 'no',
        'good morning', 'good night', 'nice to meet you'
    ]
    
    for english, ijaw in dictionary.items():
        english_lower = english.lower().strip()
        
        # Categorize based on content
        if english_lower in greetings:
            categories['greetings_and_politeness'][english] = ijaw
        elif len(english.split()) == 1:
            # Single words
            categories['basic_words'][english] = ijaw
        elif len(english.split()) <= 4 and not english.endswith('.') and not english.endswith('?'):
            # Short phrases (2-4 words, not sentences)
            categories['common_phrases'][english] = ijaw
        else:
            # Complete sentences or longer phrases
            categories['complete_sentences'][english] = ijaw
    
    return categories

def sort_categories(categories):
    """Sort each category alphabetically"""
    sorted_categories = {}
    
    for category_name, entries in categories.items():
        # Sort by English key (case-insensitive)
        sorted_entries = OrderedDict(
            sorted(entries.items(), key=lambda x: x[0].lower())
        )
        sorted_categories[category_name] = sorted_entries
    
    return sorted_categories

def create_organized_dictionary(sorted_categories):
    """Create a single organized dictionary with all entries"""
    organized_dict = OrderedDict()
    
    # Add categories in logical order
    category_order = [
        'greetings_and_politeness',
        'basic_words', 
        'common_phrases',
        'complete_sentences'
    ]
    
    for category in category_order:
        if category in sorted_categories:
            organized_dict.update(sorted_categories[category])
    
    return organized_dict

def save_organized_dictionary(organized_dict, output_path):
    """Save the organized dictionary to a JSON file"""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(organized_dict, f, ensure_ascii=False, indent=2)

def print_statistics(categories):
    """Print statistics about the categorization"""
    total_entries = sum(len(entries) for entries in categories.values())
    
    print(f"\n📊 Dictionary Organization Statistics:")
    print(f"{'='*50}")
    print(f"Total entries: {total_entries}")
    print(f"{'='*50}")
    
    for category_name, entries in categories.items():
        category_display = category_name.replace('_', ' ').title()
        print(f"{category_display}: {len(entries)} entries")
    
    print(f"{'='*50}")

def main():
    """Main function to organize the dictionary"""
    input_file = 'dictionaries/en_to_ijaw.json'
    output_file = 'dictionaries/en_to_ijaw_organized.json'
    
    print("🔄 Loading dictionary...")
    dictionary = load_dictionary(input_file)
    
    print("📂 Categorizing entries...")
    categories = categorize_entries(dictionary)
    
    print("🔤 Sorting categories alphabetically...")
    sorted_categories = sort_categories(categories)
    
    print("📝 Creating organized dictionary...")
    organized_dict = create_organized_dictionary(sorted_categories)
    
    print("💾 Saving organized dictionary...")
    save_organized_dictionary(organized_dict, output_file)
    
    print_statistics(sorted_categories)
    
    print(f"\n✅ Dictionary successfully organized!")
    print(f"📁 Original file: {input_file}")
    print(f"📁 Organized file: {output_file}")
    
    # Show sample entries from each category
    print(f"\n📋 Sample entries from each category:")
    print(f"{'='*50}")
    
    for category_name, entries in sorted_categories.items():
        if entries:
            category_display = category_name.replace('_', ' ').title()
            print(f"\n{category_display}:")
            # Show first 3 entries as examples
            for i, (english, ijaw) in enumerate(list(entries.items())[:3]):
                print(f"  • \"{english}\" → \"{ijaw}\"")
            if len(entries) > 3:
                print(f"  ... and {len(entries) - 3} more entries")

if __name__ == "__main__":
    main()