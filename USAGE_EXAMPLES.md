# 📖 Usage Examples - English → Ijaw Audio Translator

This guide provides detailed examples of how to use the English to Ijaw Audio Translator effectively.

## 🎯 Basic Usage Flow

### 1. Starting the Application

```bash
# Method 1: Use the startup script (Windows)
start_dev.bat

# Method 2: Manual startup
# Terminal 1 - Backend
cd backend
python main.py

# Terminal 2 - Frontend  
cd frontend
npm start
```

### 2. Recording Audio

1. **Open** `http://localhost:3000` in your browser
2. **Click** "Start Recording" button
3. **Speak clearly** in English (e.g., "Hello, good morning")
4. **Click** "Stop Recording" when finished
5. **Click** "Translate" to process

## 🗣️ Example Phrases to Try

### Basic Greetings

| English | Expected Ijaw | Pronunciation Guide |
|---------|---------------|-------------------|
| "Hello" | "sanma" | SAN-ma |
| "Good morning" | "duba oweikenimi" | DU-ba o-WEI-ke-ni-mi |
| "Good evening" | "duba aruowei" | DU-ba a-ru-o-WEI |
| "Thank you" | "migwo" | MIG-wo |

### Common Expressions

| English | Expected Ijaw | Context |
|---------|---------------|---------|
| "I love you" | "mi yenagha ibo" | Personal/romantic |
| "How are you" | "how ibo" | Casual greeting |
| "Where is water" | "ibo-kala beni" | Asking for directions |
| "I am hungry" | "mi nwan" | Expressing need |

### Numbers

| English | Expected Ijaw | Notes |
|---------|---------------|-------|
| "One" | "keni" | Basic counting |
| "Two" | "maa" | |
| "Three" | "taa" | |
| "Five" | "tarau" | |
| "Ten" | "pu" | |

## 🔧 Testing Different Features

### Audio Quality Test

1. **Record in quiet environment**
   - Expected: Clear transcription
   - Test phrase: "Hello, thank you very much"

2. **Record with background noise**
   - Expected: May have transcription errors
   - Solution: Use noise cancellation

3. **Record different accents**
   - Expected: Whisper handles most English accents
   - Test with various speakers

### Translation Accuracy Test

1. **Simple words** (high accuracy expected):
   ```
   "Hello" → "sanma"
   "Water" → "beni"
   "Food" → "kibo"
   ```

2. **Complex phrases** (may need improvement):
   ```
   "I want to go to the market" → Mixed results
   "The weather is beautiful today" → Partial translation
   ```

3. **Unknown words** (fallback behavior):
   ```
   "Refrigerator" → "refrigerator" (unchanged)
   "Computer" → "computer" (unchanged)
   ```

## 📊 Expected Results

### Successful Translation Example

**Input Audio**: "Hello, good morning"

**Expected Output**:
```json
{
  "english_text": "Hello, good morning",
  "ijaw_text": "sanma duba oweikenimi",
  "audio_filename": "ijaw_audio_abc123.wav",
  "audio_url": "/audio/ijaw_audio_abc123.wav"
}
```

**Audio Playback**: Synthetic tones representing each Ijaw word

### Partial Translation Example

**Input Audio**: "Hello, I need a computer"

**Expected Output**:
```json
{
  "english_text": "Hello, I need a computer",
  "ijaw_text": "sanma mi computer",
  "audio_filename": "ijaw_audio_def456.wav",
  "audio_url": "/audio/ijaw_audio_def456.wav"
}
```

**Note**: "computer" remains untranslated (not in dictionary)

## 🧪 API Testing

### Direct API Testing

You can test the backend API directly using curl or Postman:

```bash
# Test basic endpoint
curl http://localhost:8000/

# Get dictionary
curl http://localhost:8000/dictionary

# Add new translation
curl -X POST "http://localhost:8000/dictionary/add" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "english_word=computer&ijaw_word=komputa"
```

### Audio File Testing

```bash
# Test audio endpoint
curl http://localhost:8000/audio/sample_audio.wav --output test.wav

# Upload audio file for translation
curl -X POST "http://localhost:8000/translate" \
  -H "Content-Type: multipart/form-data" \
  -F "audio_file=@test_audio.wav"
```

## 🎨 Frontend Testing

### UI Component Testing

1. **Recording Button States**:
   - ✅ "Start Recording" (initial state)
   - ✅ "Stop Recording" (while recording)
   - ✅ Disabled during translation

2. **Visual Feedback**:
   - ✅ Recording indicator with timer
   - ✅ Loading spinner during translation
   - ✅ Success message after recording

3. **Error Handling**:
   - ✅ Microphone permission denied
   - ✅ Backend connection failed
   - ✅ Translation timeout

### Browser Compatibility Testing

| Browser | Recording | Translation | Audio Playback | Notes |
|---------|-----------|-------------|----------------|-------|
| Chrome 90+ | ✅ | ✅ | ✅ | Best performance |
| Firefox 88+ | ✅ | ✅ | ✅ | Good compatibility |
| Safari 14+ | ✅ | ✅ | ⚠️ | May need user interaction |
| Edge 90+ | ✅ | ✅ | ✅ | Similar to Chrome |

## 🔍 Performance Testing

### Response Time Expectations

| Operation | Expected Time | Factors |
|-----------|---------------|---------|
| Audio Recording | Real-time | Browser performance |
| Whisper Transcription | 2-10 seconds | Audio length, model size |
| Dictionary Translation | <1 second | Dictionary size |
| Audio Generation | 1-3 seconds | Number of words |
| Total Process | 5-15 seconds | Combined factors |

### Load Testing

```bash
# Test multiple concurrent requests
for i in {1..5}; do
  curl -X POST "http://localhost:8000/translate" \
    -F "audio_file=@test.wav" &
done
```

## 🐛 Common Issues and Solutions

### Issue: Poor Transcription Quality

**Symptoms**: English text is incorrect or garbled

**Solutions**:
1. Speak more clearly and slowly
2. Reduce background noise
3. Use better microphone
4. Try shorter phrases
5. Switch to larger Whisper model

**Test**:
```bash
# Try with different Whisper models
# Edit backend/main.py:
whisper_model = whisper.load_model("small")  # Better accuracy
```

### Issue: Missing Translations

**Symptoms**: English words appear in Ijaw output

**Solutions**:
1. Add words to dictionary
2. Use simpler vocabulary
3. Check spelling in dictionary

**Test**:
```bash
# Add missing word via API
curl -X POST "http://localhost:8000/dictionary/add" \
  -d "english_word=house&ijaw_word=wari"
```

### Issue: No Audio Playback

**Symptoms**: Translation appears but no sound

**Solutions**:
1. Check browser audio permissions
2. Verify audio files exist
3. Test with different browser
4. Check volume settings

**Test**:
```bash
# Verify audio files generated
ls backend/output_audio/
ls backend/audio_files/
```

## 📈 Improvement Suggestions

### Dictionary Expansion

1. **Add more common words**:
   ```json
   {
     "please": "biko",
     "sorry": "sorry",
     "excuse": "excuse",
     "help": "help"
   }
   ```

2. **Add phrases and idioms**:
   ```json
   {
     "how are you": "how ibo dey",
     "what is your name": "wetin be your name",
     "nice to meet you": "nice to meet ibo"
   }
   ```

### Audio Quality Enhancement

1. **Record with native speakers**
2. **Use professional recording equipment**
3. **Normalize audio levels**
4. **Add pronunciation variations**

### Grammar Improvements

1. **Implement SOV word order**
2. **Add verb conjugations**
3. **Handle plurals correctly**
4. **Add tense markers**

## 🎯 Success Metrics

### Translation Quality

- **Word Coverage**: 70%+ of common English words
- **Accuracy**: 80%+ for covered words
- **Grammar**: Basic SOV structure

### User Experience

- **Response Time**: <15 seconds end-to-end
- **Error Rate**: <5% for supported phrases
- **Usability**: Intuitive interface

### Technical Performance

- **Uptime**: 99%+ availability
- **Concurrent Users**: 10+ simultaneous
- **Resource Usage**: <2GB RAM, <50% CPU

## 🚀 Next Steps

1. **Expand dictionary** with more Ijaw words
2. **Record authentic audio** with native speakers
3. **Implement grammar rules** for better translation
4. **Add user feedback** system
5. **Deploy to production** environment

---

**Happy testing! 🧪✨**

For more detailed technical information, see the main README.md file.