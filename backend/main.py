from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
import os
import tempfile
import uuid
import logging
from typing import Dict, List, Optional
import re
from ijaw_grammar import IjawGrammarEngine
from TTS import synthesize_speech

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="English to Ijaw Audio Translator", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
en_to_ijaw_dict = {}
audio_dict = {}
grammar_engine = None

# Directories
AUDIO_DIR = "audio_files"
DICT_DIR = "dictionaries"
OUTPUT_DIR = "output_audio"
TTS_LANG = os.getenv("TTS_LANG", "en")

# Ensure directories exist
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(DICT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_speech_recognition():
    """Safely import speech_recognition; return None if unavailable.

    On Python 3.13 the standard library module 'aifc' was removed, which
    causes speech_recognition to fail to import. Returning None lets the
    app start and endpoints provide a graceful message instead of crashing.
    """
    try:
        import speech_recognition as sr  # type: ignore
        return sr
    except Exception as e:
        logger.error(f"Speech recognition unavailable: {e}")
        return None

def load_dictionaries():
    """Load English to Ijaw dictionary and audio mappings"""
    global en_to_ijaw_dict, audio_dict, grammar_engine
    
    # Load translation dictionary
    dict_path = os.path.join(DICT_DIR, "en_to_ijaw.json")
    if os.path.exists(dict_path):
        with open(dict_path, 'r', encoding='utf-8') as f:
            en_to_ijaw_dict = json.load(f)
        logger.info(f"Loaded {len(en_to_ijaw_dict)} translations")
    else:
        logger.warning(f"Dictionary not found at {dict_path}")
    
    # Load audio dictionary
    audio_dict_path = os.path.join(DICT_DIR, "audio_dict.json")
    if os.path.exists(audio_dict_path):
        with open(audio_dict_path, 'r', encoding='utf-8') as f:
            audio_dict = json.load(f)
        logger.info(f"Loaded {len(audio_dict)} audio mappings")
    else:
        logger.warning(f"Audio dictionary not found at {audio_dict_path}")
    
    # Initialize grammar engine for intelligent translation
    try:
        grammar_engine = IjawGrammarEngine(dict_path)
        grammar_info = grammar_engine.get_grammar_info()
        logger.info(f"Grammar engine initialized with {grammar_info['patterns_count']} patterns")
        logger.info(f"Loaded {grammar_info['pronouns_count']} pronouns, {grammar_info['verbs_count']} verbs, {grammar_info['nouns_count']} nouns")
    except Exception as e:
        logger.warning(f"Grammar engine initialization failed: {e}")
        grammar_engine = None

def translate_to_ijaw(english_text: str) -> str:
    """Translate English text to Ijaw with intelligent grammar-based generation"""
    if not english_text:
        return ""
    
    # Clean and normalize the input
    text = english_text.strip().lower()
    
    # First, try to find a complete phrase match in dictionary
    if text in en_to_ijaw_dict:
        return en_to_ijaw_dict[text]
    
    # Use grammar engine for intelligent translation if available
    if grammar_engine:
        try:
            generated_translation = grammar_engine.generate_translation(english_text)
            # If the grammar engine produced a meaningful translation (not just word-by-word fallback)
            if generated_translation and generated_translation != english_text:
                return generated_translation
        except Exception as e:
            logger.warning(f"Grammar engine translation failed: {e}")
    
    # Fallback to word-by-word translation
    words = text.split()
    translated_words = []
    
    for word in words:
        # Remove punctuation for lookup
        clean_word = re.sub(r'[^\w\s]', '', word)
        
        # Look up the word in the dictionary
        if clean_word in en_to_ijaw_dict:
            translated_words.append(en_to_ijaw_dict[clean_word])
        else:
            # Keep the original word if no translation found
            translated_words.append(word)
    
    return " ".join(translated_words)

def transcribe_audio(audio_file_path: str) -> str:
    """
    Transcribe audio file to text using speech recognition
    Supports: WAV, AIFF/AIFF-C, and Native FLAC files only
    """
    logger.info(f"Processing audio file: {audio_file_path}")
    
    try:
        # Initialize recognizer (lazy import to avoid boot-time failures)
        sr = get_speech_recognition()
        if sr is None:
            logger.error("speech_recognition could not be imported (likely missing 'aifc' on Python 3.13)")
            return (
                "Speech recognition is not available on this deployment. "
                "Please use text translation or upload WAV/AIFF when the service is enabled."
            )
        recognizer = sr.Recognizer()
        
        # Check if file exists
        if not os.path.exists(audio_file_path):
            logger.error(f"Audio file not found: {audio_file_path}")
            return "Audio file not found. Please try again."
        
        # Check file extension for supported formats
        file_ext = os.path.splitext(audio_file_path)[1].lower()
        supported_formats = ['.wav', '.aiff', '.aif', '.aifc', '.flac']
        
        if file_ext not in supported_formats:
            logger.warning(f"Unsupported audio format: {file_ext}")
            return f"Unsupported audio format ({file_ext}). Please upload a WAV, AIFF, or FLAC file."
        
        # Process the audio file with speech_recognition
        try:
            logger.info("Processing audio with speech_recognition...")
            with sr.AudioFile(audio_file_path) as source:
                logger.info("Reading audio file...")
                # Adjust for ambient noise
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Record the audio
                audio_data = recognizer.record(source)
            
            logger.info("Audio processing successful, proceeding with recognition...")
            
        except Exception as processing_error:
            logger.error(f"Audio processing failed: {processing_error}")
            return "Error reading audio file. Please ensure the file is not corrupted and try again."
        
        # Recognize speech using Google Speech Recognition
        try:
            logger.info("Sending audio to Google Speech Recognition...")
            text = recognizer.recognize_google(audio_data)
            logger.info(f"Speech recognition successful: {text}")
            return text.lower().strip()
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return "Sorry, I could not understand the audio. Please speak clearly."
        except sr.RequestError as e:
            logger.error(f"Could not request results from Google Speech Recognition service: {e}")
            return "Speech recognition service is currently unavailable."
            
    except Exception as e:
        logger.error(f"Error processing audio file: {e}")
        return "Error processing audio file. Please try again."

def generate_audio_from_text(ijaw_text: str) -> str:
    """
    Generate audio from text using gTTS (MP3 output).
    Falls back to empty WAV if gTTS fails.
    """
    try:
        filename = synthesize_speech(ijaw_text, lang=TTS_LANG, slow=False)
        return filename
    except Exception as e:
        logger.warning(f"gTTS failed, falling back to empty WAV: {e}")
        # Fallback empty WAV
        audio_id = str(uuid.uuid4())[:8]
        filename = f"ijaw_audio_{audio_id}.wav"
        filepath = os.path.join(OUTPUT_DIR, filename)
        wav_header = bytes([
            0x52, 0x49, 0x46, 0x46,
            0x24, 0x00, 0x00, 0x00,
            0x57, 0x41, 0x56, 0x45,
            0x66, 0x6D, 0x74, 0x20,
            0x10, 0x00, 0x00, 0x00,
            0x01, 0x00,
            0x01, 0x00,
            0x44, 0xAC, 0x00, 0x00,
            0x88, 0x58, 0x01, 0x00,
            0x02, 0x00,
            0x10, 0x00,
            0x64, 0x61, 0x74, 0x61,
            0x00, 0x00, 0x00, 0x00
        ])
        with open(filepath, 'wb') as f:
            f.write(wav_header)
        return filename

@app.on_event("startup")
async def startup_event():
    logger.info("Starting English to Ijaw Audio Translator...")
    # Attempt speech recognition import to log availability at startup
    if get_speech_recognition() is None:
        logger.warning("Speech recognition unavailable (missing 'aifc' on Python 3.13). API will still start.")
    else:
        logger.info("Speech recognition available - ready for audio transcription")
    
    load_dictionaries()
    logger.info("Startup complete - ready for real translation")

@app.get("/")
async def root():
    return {"message": "English to Ijaw Audio Translator API", "status": "running"}

@app.post("/translate")
async def translate_audio(audio_file: UploadFile = File(...)):
    """
    Main translation endpoint:
    1. Receive audio file
    2. Transcribe using speech recognition
    3. Translate to Ijaw
    4. Generate mock Ijaw audio
    5. Return translation and audio filename
    """
    temp_file_exists = False
    temp_file_path = None
    
    try:
        # Validate file type
        if not audio_file.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Get file extension from original filename
        original_filename = audio_file.filename or "audio.wav"
        file_extension = os.path.splitext(original_filename)[1].lower()
        
        # Check if the file format is supported by speech_recognition
        supported_extensions = ['.wav', '.aiff', '.aif', '.aifc', '.flac']
        if file_extension not in supported_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported audio format: {file_extension}. Supported formats: WAV, AIFF, FLAC"
            )
        
        # Save uploaded file temporarily with correct extension
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            content = await audio_file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        temp_file_exists = True
        try:
            # Real transcription using speech recognition
            logger.info("Transcribing audio using speech recognition...")
            english_text = transcribe_audio(temp_file_path)
            
            # Check if transcription was successful
            if english_text.startswith("Error") or english_text.startswith("Sorry"):
                logger.warning(f"Transcription issue: {english_text}")
                # Don't raise exception, just return the message
            
            logger.info(f"Transcribed: {english_text}")
            
            # Translate to Ijaw
            logger.info("Translating to Ijaw...")
            ijaw_text = translate_to_ijaw(english_text)
            logger.info(f"Translated: {ijaw_text}")
            
            # Generate Ijaw audio
            logger.info("Generating Ijaw audio...")
            audio_filename = generate_audio_from_text(ijaw_text)
            logger.info(f"Generated audio: {audio_filename}")
            
            return {
                "english_text": english_text,
                "ijaw_text": ijaw_text,
                "audio_filename": audio_filename,
                "audio_url": f"/audio/{audio_filename}",
                "status": "success"
            }
            
        finally:
            # Clean up temporary file
            if temp_file_exists and temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.unlink(temp_file_path)
                except Exception as cleanup_error:
                    logger.warning(f"Could not clean up temp file: {cleanup_error}")
            
    except HTTPException:
        # Re-raise HTTPExceptions (like 400 errors) without modification
        raise
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        logger.error(f"Translation error: {e}")
        logger.error(f"Full traceback: {error_traceback}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    """Serve generated audio files (MP3 or WAV)"""
    file_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio file not found")
    ext = os.path.splitext(filename)[1].lower()
    media = "audio/mpeg" if ext == ".mp3" else "audio/wav"
    return FileResponse(file_path, media_type=media, filename=filename)

@app.get("/dictionary")
async def get_dictionary():
    """Get current dictionary for debugging/expansion"""
    return {
        "translation_dict": en_to_ijaw_dict,
        "audio_dict": audio_dict,
        "translation_count": len(en_to_ijaw_dict),
        "audio_count": len(audio_dict)
    }

@app.post("/dictionary/add")
async def add_translation(english_word: str, ijaw_word: str):
    """Add new translation to dictionary"""
    en_to_ijaw_dict[english_word.lower()] = ijaw_word
    
    # Save updated dictionary
    dict_path = os.path.join(DICT_DIR, "en_to_ijaw.json")
    with open(dict_path, 'w', encoding='utf-8') as f:
        json.dump(en_to_ijaw_dict, f, ensure_ascii=False, indent=2)
    
    return {"message": f"Added translation: {english_word} -> {ijaw_word}"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "dictionaries_loaded": len(en_to_ijaw_dict) > 0,
        "translation_count": len(en_to_ijaw_dict)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)