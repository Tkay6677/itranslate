#!/usr/bin/env python3
"""
Ijaw Grammar Engine for Intelligent Translation Generation

This module implements grammatical rules and sentence generation for Ijaw (Izon) language
following the Subject-Object-Verb (SOV) structure and other linguistic patterns.
"""

import json
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class WordType(Enum):
    SUBJECT = "subject"
    OBJECT = "object"
    VERB = "verb"
    ADJECTIVE = "adjective"
    PRONOUN = "pronoun"
    NOUN = "noun"
    PREPOSITION = "preposition"
    DETERMINER = "determiner"
    UNKNOWN = "unknown"

@dataclass
class IjawWord:
    english: str
    ijaw: str
    word_type: WordType
    variations: List[str] = None

class IjawGrammarEngine:
    def __init__(self, dictionary_path: str):
        self.dictionary = self.load_dictionary(dictionary_path)
        self.word_mappings = {}
        self.grammar_patterns = {}
        self.pronouns = {}
        self.verbs = {}
        self.nouns = {}
        self.adjectives = {}
        
        self._analyze_dictionary()
        self._setup_grammar_rules()
    
    def load_dictionary(self, path: str) -> Dict[str, str]:
        """Load the dictionary from JSON file"""
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _analyze_dictionary(self):
        """Analyze dictionary to extract grammatical patterns"""
        
        # Extract pronouns
        self.pronouns = {
            "I": "Arí",
            "you": "Ị", 
            "he": "U",
            "she": "A",
            "we": "Wónì",
            "they": "Wónì",
            "my": "yè",
            "your": "wè",
            "his": "yè",
            "her": "yè",
            "our": "wónì",
            "their": "wónì"
        }
        
        # Extract common verbs and their patterns
        self.verbs = {
            "am": "ye",
            "is": "ye", 
            "are": "ye",
            "have": "sabi",
            "has": "sabi",
            "want": "wọnt",
            "wants": "wọnt",
            "like": "laik",
            "likes": "laik",
            "see": "fịnị",
            "sees": "fịnị",
            "eat": "fị",
            "eats": "fị",
            "drink": "mu",
            "drinks": "mu",
            "go": "gha",
            "goes": "gha",
            "come": "bia",
            "comes": "bia",
            "work": "wok",
            "works": "wok",
            "sleep": "turu",
            "sleeps": "turu",
            "build": "bil",
            "builds": "bil",
            "take": "akị́",
            "takes": "akị́",
            "give": "giv",
            "gives": "giv",
            "help": "help",
            "helps": "help",
            "walk": "waka",
            "walks": "waka",
            "run": "ron",
            "runs": "ron",
            "dance": "dans",
            "dances": "dans",
            "sing": "son",
            "sings": "son",
            "cook": "nkọ̀rọ",
            "cooks": "nkọ̀rọ"
        }
        
        # Extract common nouns
        self.nouns = {
            "house": "wárị",
            "water": "bení",
            "food": "fị́yaị",
            "fish": "ìndí",
            "river": "ọ́wụ",
            "sun": "sọ́",
            "moon": "akalụ́",
            "child": "tọ́bọ̀ụ",
            "friend": "kẹ́nị",
            "family": "wárịbịbị̀",
            "father": "owéi",
            "mother": "ẹ́rẹ",
            "brother": "bàrà",
            "sister": "eréwèrí",
            "money": "abadị-ugú",
            "yam": "òkù-ị̀wẹ",
            "cassava": "abábùrú",
            "canoe": "òrù",
            "cup": "agbéì",
            "net": "agbunú",
            "market": "maket",
            "village": "òkù-ámà",
            "farm": "ògbó",
            "fire": "faya",
            "ancestor": "ìwéi",
            "ancestors": "ìwéi-wónì",  # plural form
            "children": "tọ́bọ̀ụ-wónì",
            "friends": "kẹ́nị-wónì",
            "people": "òkù-wónì"
        }
        
        # Extract adjectives
        self.adjectives = {
            "good": "botu",
            "bad": "kiri",
            "big": "toru",
            "small": "kiri-kiri",
            "happy": "hapi",
            "tired": "sik",
            "strong": "strong",
            "wise": "akíròro",
            "kind": "botu",
            "busy": "wok haad",
            "hungry": "hongri",
            "thirsty": "tosti",
            "hot": "tuu dọ́n",
            "cold": "kol",
            "clean": "klin",
            "fresh": "nyu",
            "warm": "hot",
            "bright": "rait",
            "deep": "tọ́n",
            "long": "pórù",
            "tall": "toru",
            "beautiful": "fain",
            "angry": "kírimá",  # derived from "anger"
            "sad": "kiri",
            "old": "òkú",
            "young": "tọ́bọ̀ụ",
            "new": "nyu",
            "fast": "fast",
            "slow": "slow",
            "sick": "sik"
        }
    
    def _setup_grammar_rules(self):
        """Setup Ijaw grammatical rules and patterns"""
        
        # SOV patterns for different sentence types
        self.grammar_patterns = {
            # Subject + Verb patterns
            "subject_verb": "{subject} {verb}",
            
            # Subject + Object + Verb (SOV)
            "subject_object_verb": "{subject} {object} {verb}",
            
            # Subject + Adjective patterns  
            "subject_adjective": "{subject} {adjective} ye",
            
            # Subject + has/have + Object
            "subject_have_object": "{subject} {object} sabi",
            
            # Subject + want + Object
            "subject_want_object": "{subject} {object} wọnt",
            
            # Subject + like + Object
            "subject_like_object": "{subject} {object} laik",
            
            # Possessive patterns
            "possessive_noun": "{possessive} {noun}",
            
            # Location patterns
            "subject_at_location": "{subject} {location} ye",
            
            # Direction patterns  
            "subject_go_location": "{subject} {location} gha",
            "subject_come_location": "{subject} {location} bia",
            
            # Time patterns
            "subject_verb_time": "{subject} {verb} {time}",
            
            # Question patterns
            "where_is": "{object} kí ye?",
            "how_are": "I bódọụ?",
            "do_you_have": "Ị {object} sabi?",
            
            # Compound sentences
            "subject_verb_with_object": "{subject} {object} {verb}",
            "subject_verb_adverb": "{subject} {verb} {adverb}"
        }
    
    def classify_word(self, word: str) -> WordType:
        """Classify an English word by type"""
        word_lower = word.lower()
        
        if word_lower in self.pronouns:
            return WordType.PRONOUN
        elif word_lower in self.verbs:
            return WordType.VERB
        elif word_lower in self.nouns:
            return WordType.NOUN
        elif word_lower in self.adjectives:
            return WordType.ADJECTIVE
        elif word_lower in ["the", "a", "an", "this", "that"]:
            return WordType.DETERMINER
        elif word_lower in ["to", "at", "in", "on", "with", "from"]:
            return WordType.PREPOSITION
        else:
            return WordType.UNKNOWN
    
    def translate_word(self, word: str) -> str:
        """Translate a single word to Ijaw"""
        word_lower = word.lower()
        
        # Check direct dictionary lookup first
        if word_lower in self.dictionary:
            return self.dictionary[word_lower]
        
        # Check specific word type mappings
        if word_lower in self.pronouns:
            return self.pronouns[word_lower]
        elif word_lower in self.verbs:
            return self.verbs[word_lower]
        elif word_lower in self.nouns:
            return self.nouns[word_lower]
        elif word_lower in self.adjectives:
            return self.adjectives[word_lower]
        
        # Return original word if no translation found
        return word
    
    def parse_sentence(self, sentence: str) -> Dict:
        """Parse an English sentence to identify components"""
        words = sentence.lower().strip().split()
        parsed = {
            "subject": None,
            "object": None,
            "verb": None,
            "adjective": None,
            "preposition": None,
            "location": None,
            "time": None,
            "question_type": None
        }
        
        # Simple parsing logic
        for i, word in enumerate(words):
            word_type = self.classify_word(word)
            
            # Don't treat possessive pronouns as subjects
            if word_type == WordType.PRONOUN and not parsed["subject"] and word not in ["my", "your", "his", "her", "our", "their"]:
                parsed["subject"] = word
            elif word_type == WordType.VERB and not parsed["verb"]:
                parsed["verb"] = word
            elif word_type == WordType.NOUN:
                if not parsed["object"]:
                    parsed["object"] = word
                elif word in ["house", "market", "river", "village", "farm"]:
                    parsed["location"] = word
            elif word_type == WordType.ADJECTIVE and not parsed["adjective"]:
                parsed["adjective"] = word
            elif word in ["now", "today", "tomorrow", "early", "late"]:
                parsed["time"] = word
        
        # Detect question patterns
        if sentence.startswith("where"):
            parsed["question_type"] = "where"
        elif sentence.startswith("how are"):
            parsed["question_type"] = "how_are"
        elif sentence.startswith("do you have"):
            parsed["question_type"] = "do_you_have"
        
        return parsed
    
    def generate_translation(self, sentence: str) -> str:
        """Generate Ijaw translation using grammatical rules"""
        
        # First check if exact phrase exists in dictionary
        sentence_lower = sentence.lower().strip()
        if sentence_lower in self.dictionary:
            return self.dictionary[sentence_lower]
        
        # Parse the sentence
        parsed = self.parse_sentence(sentence)
        
        # Generate translation based on patterns
        if parsed["question_type"] == "how_are":
            return "I bódọụ?"
        elif parsed["question_type"] == "where" and parsed["object"]:
            obj_translation = self.translate_word(parsed["object"])
            return f"{obj_translation} kí ye?"
        elif parsed["question_type"] == "do_you_have" and parsed["object"]:
            obj_translation = self.translate_word(parsed["object"])
            return f"Ị {obj_translation} sabi?"
        
        # Handle statements with improved SOV structure
        if parsed["subject"] and parsed["adjective"]:
            # Subject + Adjective pattern: "I am happy" -> "Arí hapi ye"
            subj = self.translate_word(parsed["subject"])
            adj = self.translate_word(parsed["adjective"])
            return f"{subj} {adj} ye"
        
        elif parsed["subject"] and parsed["object"] and parsed["verb"]:
            # SOV pattern: Subject + Object + Verb
            subj = self.translate_word(parsed["subject"])
            obj = self.translate_word(parsed["object"])
            verb = self.translate_word(parsed["verb"])
            
            # Special handling for specific verbs
            if parsed["verb"] in ["have", "has"]:
                return f"{subj} {obj} sabi"
            elif parsed["verb"] in ["want", "wants"]:
                return f"{subj} {obj} wọnt"
            elif parsed["verb"] in ["like", "likes"]:
                return f"{subj} {obj} laik"
            elif parsed["verb"] in ["eat", "eats"]:
                return f"{subj} {obj} fị"
            elif parsed["verb"] in ["build", "builds"]:
                return f"{subj} {obj} bil"
            else:
                return f"{subj} {obj} {verb}"
        
        elif parsed["subject"] and parsed["verb"]:
            # Subject + Verb pattern
            subj = self.translate_word(parsed["subject"])
            verb = self.translate_word(parsed["verb"])
            
            # Handle location-based verbs
            if parsed["location"]:
                loc = self.translate_word(parsed["location"])
                if parsed["verb"] in ["go", "goes"]:
                    return f"{subj} {loc} gha"
                elif parsed["verb"] in ["come", "comes"]:
                    return f"{subj} {loc} bia"
                elif parsed["verb"] in ["walk", "walks"]:
                    return f"{subj} {loc} waka"
                else:
                    return f"{subj} {loc} {verb}"
            
            # Handle time-based expressions
            if parsed["time"]:
                time_word = self.translate_word(parsed["time"])
                return f"{subj} {time_word} {verb}"
            
            # Handle "to be" verbs specially
            if parsed["verb"] in ["am", "is", "are"]:
                return f"{subj} ye"
            
            return f"{subj} {verb}"
        
        # Handle possessive patterns: "my father" -> "owéi yè"
        words = sentence_lower.split()
        if len(words) >= 2:
            if words[0] in ["my", "your", "his", "her", "our", "their"]:
                possessive = self.translate_word(words[0])
                noun = self.translate_word(words[1])
                if len(words) == 2:
                    return f"{noun} {possessive}"
                elif len(words) == 3 and words[2] in ["is", "are"]:
                    return f"{noun} {possessive} ye"
                elif len(words) >= 3:
                    # Handle "my ancestors are angry" -> "yè ìwéi-wónì kírimá ye" (SOV)
                    if words[2] in ["is", "are"] and len(words) == 4 and words[3] in self.adjectives:
                        adj = self.translate_word(words[3])
                        return f"{possessive} {noun} {adj} ye"
                    elif words[2] in ["is", "are"] and len(words) == 4:
                        adj = self.translate_word(words[3])
                        return f"{noun} {possessive} {adj} ye"
                    else:
                        rest = " ".join([self.translate_word(w) for w in words[2:]])
                        return f"{noun} {possessive} {rest}"
        
        # Fallback: word-by-word translation
        words = sentence.split()
        translated_words = [self.translate_word(word) for word in words]
        return " ".join(translated_words)
    
    def get_grammar_info(self) -> Dict:
        """Return information about loaded grammar rules"""
        return {
            "pronouns_count": len(self.pronouns),
            "verbs_count": len(self.verbs),
            "nouns_count": len(self.nouns),
            "adjectives_count": len(self.adjectives),
            "patterns_count": len(self.grammar_patterns),
            "total_dictionary_entries": len(self.dictionary)
        }

def test_grammar_engine():
    """Test the grammar engine with sample sentences"""
    engine = IjawGrammarEngine("dictionaries/en_to_ijaw.json")
    
    test_sentences = [
        "I am happy",
        "You have water", 
        "He likes fish",
        "She goes home",
        "We eat food",
        "They build house",
        "Where is the river?",
        "How are you?",
        "Do you have money?",
        "My father is strong",
        "The child sleeps now",
        "I want to eat",
        "She walks to market"
    ]
    
    print("🧠 Ijaw Grammar Engine Test Results:")
    print("=" * 50)
    
    for sentence in test_sentences:
        translation = engine.generate_translation(sentence)
        print(f"EN: {sentence}")
        print(f"IJ: {translation}")
        print("-" * 30)
    
    info = engine.get_grammar_info()
    print(f"\n📊 Grammar Engine Statistics:")
    for key, value in info.items():
        print(f"{key.replace('_', ' ').title()}: {value}")

if __name__ == "__main__":
    test_grammar_engine()