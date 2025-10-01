#!/usr/bin/env python3
"""
Sample audio file generator for Ijaw words
This script creates basic audio files for testing the translator.
In production, these would be replaced with actual recordings by native speakers.
"""

import os
import json
from pydub import AudioSegment
from pydub.generators import Sine, Square, Sawtooth
import random

def create_sample_audio_files():
    """Create sample audio files for Ijaw words using synthetic tones"""
    
    # Ensure audio directory exists
    audio_dir = "audio_files"
    os.makedirs(audio_dir, exist_ok=True)
    
    # Load the audio dictionary to know which files to create
    with open("dictionaries/audio_dict.json", 'r', encoding='utf-8') as f:
        audio_dict = json.load(f)
    
    # Create sample audio for each word
    for ijaw_word, filename in audio_dict.items():
        file_path = os.path.join(audio_dir, filename)
        
        if not os.path.exists(file_path):
            print(f"Creating audio for: {ijaw_word} -> {filename}")
            
            # Create a unique tone pattern for each word
            # This is just for testing - real implementation would use actual recordings
            word_length = len(ijaw_word)
            syllables = max(1, word_length // 3)  # Estimate syllables
            
            segments = []
            base_freq = 200 + (hash(ijaw_word) % 400)  # Frequency based on word hash
            
            for i in range(syllables):
                # Vary frequency for each syllable
                freq = base_freq + (i * 50)
                duration = 300 + (len(ijaw_word) * 20)  # Duration based on word length
                
                # Use different waveforms for variety
                if i % 3 == 0:
                    tone = Sine(freq).to_audio_segment(duration=duration)
                elif i % 3 == 1:
                    tone = Square(freq).to_audio_segment(duration=duration)
                else:
                    tone = Sawtooth(freq).to_audio_segment(duration=duration)
                
                # Apply fade in/out for smoother sound
                tone = tone.fade_in(50).fade_out(50)
                segments.append(tone)
                
                # Add small pause between syllables
                if i < syllables - 1:
                    segments.append(AudioSegment.silent(duration=100))
            
            # Combine all segments
            final_audio = sum(segments) if segments else Sine(440).to_audio_segment(duration=500)
            
            # Normalize volume
            final_audio = final_audio.normalize()
            
            # Export as WAV
            final_audio.export(file_path, format="wav")
    
    print(f"Created {len(audio_dict)} sample audio files in {audio_dir}/")

def create_common_words_audio():
    """Create audio files for the most common words with better quality"""
    
    common_words = {
        "sanma": "hello",
        "migwo": "thank you", 
        "duba": "good",
        "ee": "yes",
        "kpai": "no",
        "beni": "water",
        "kibo": "food"
    }
    
    audio_dir = "audio_files"
    
    for ijaw_word, english_meaning in common_words.items():
        filename = f"{ijaw_word}.wav"
        file_path = os.path.join(audio_dir, filename)
        
        print(f"Creating enhanced audio for common word: {ijaw_word} ({english_meaning})")
        
        # Create a more pleasant tone sequence for common words
        segments = []
        
        # Create a melody-like pattern
        if ijaw_word == "sanma":  # hello - rising tone
            freqs = [262, 330, 392]  # C, E, G
        elif ijaw_word == "migwo":  # thank you - grateful tone
            freqs = [392, 330, 262, 330]  # G, E, C, E
        elif ijaw_word == "duba":  # good - positive tone
            freqs = [330, 392, 440]  # E, G, A
        elif ijaw_word == "ee":  # yes - affirmative
            freqs = [440, 523]  # A, C
        elif ijaw_word == "kpai":  # no - declining tone
            freqs = [392, 330, 262]  # G, E, C
        else:
            # Default pattern
            freqs = [330, 392, 330]
        
        for freq in freqs:
            tone = Sine(freq).to_audio_segment(duration=200)
            tone = tone.fade_in(30).fade_out(30)
            segments.append(tone)
            segments.append(AudioSegment.silent(duration=50))
        
        final_audio = sum(segments).normalize()
        final_audio.export(file_path, format="wav")

if __name__ == "__main__":
    print("Generating sample audio files for Ijaw words...")
    create_sample_audio_files()
    create_common_words_audio()
    print("Sample audio generation complete!")
    print("\nNote: These are synthetic audio files for testing.")
    print("For production use, replace with recordings by native Ijaw speakers.")