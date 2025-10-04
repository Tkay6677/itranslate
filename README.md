# 🎤 English → Ijaw Audio Translator

A web-based prototype that translates English speech to Ijaw language with audio output. This application uses Whisper ASR for speech recognition, dictionary-based translation, and audio concatenation for Ijaw speech synthesis.

## 🌟 Features

- **🎙️ Voice Recording**: Record English speech directly in the browser
- **📝 Speech-to-Text**: Convert English audio to text using OpenAI Whisper
- **🔄 Translation**: Translate English text to Ijaw using a comprehensive dictionary
- **🔊 Audio Synthesis**: Generate Ijaw audio using pre-recorded word files
- **🎨 Modern UI**: Beautiful, responsive React frontend
- **⚡ Real-time Processing**: Fast translation and audio generation

## 📁 Project Structure

```
itranslate/
├── backend/                    # FastAPI backend
│   ├── main.py                # Main FastAPI application
│   ├── requirements.txt       # Python dependencies
│   ├── generate_sample_audio.py # Audio file generator
│   ├── dictionaries/          # Translation dictionaries
│   │   ├── en_to_ijaw.json   # English to Ijaw dictionary
│   │   └── audio_dict.json   # Audio file mappings
│   ├── audio_files/          # Pre-recorded Ijaw word audio files
│   └── output_audio/         # Generated translation audio files
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── App.js            # Main React component
│   │   ├── App.css           # Styling
│   │   ├── index.js          # React entry point
│   │   └── index.css         # Global styles
│   ├── public/
│   │   ├── index.html        # HTML template
│   │   └── manifest.json     # PWA manifest
│   └── package.json          # Node.js dependencies
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **FFmpeg** (for audio processing)
- **Microphone access** (for recording)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   
   # Windows
   venv\\Scripts\\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate sample audio files:**
   ```bash
   python generate_sample_audio.py
   ```

5. **Start the FastAPI server:**
   ```bash
   python main.py
   ```
   
   The backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the React development server:**
   ```bash
   npm start
   ```
   
   The frontend will be available at `http://localhost:3000`

## 🎯 Usage

1. **Open your browser** and go to `http://localhost:3000`
2. **Click "Start Recording"** and speak in English
3. **Click "Stop Recording"** when finished
4. **Click "Translate"** to process your speech
5. **Listen to the Ijaw translation** using the audio player

### Example Phrases to Try

- "Hello, good morning"
- "Thank you very much"
- "I love you"
- "Where is the water?"
- "How are you today?"

## 🔧 API Endpoints

### Backend API (`http://localhost:8000`)

- **POST `/translate`**: Upload audio file and get translation
  - Input: Audio file (multipart/form-data)
  - Output: JSON with English text, Ijaw translation, and audio filename

- **GET `/audio/{filename}`**: Download generated Ijaw audio file
  - Input: Audio filename
  - Output: WAV audio file

- **GET `/dictionary`**: Get current translation dictionaries
  - Output: JSON with translation and audio dictionaries

- **POST `/dictionary/add`**: Add new translation
  - Input: `english_word`, `ijaw_word`
  - Output: Confirmation message

## 📚 Expanding the Dictionary

### Adding New Translations

1. **Edit the dictionary file:**
   ```bash
   # Edit backend/dictionaries/en_to_ijaw.json
   {
     "new_english_word": "new_ijaw_translation",
     ...
   }
   ```

2. **Add corresponding audio file:**
   ```bash
   # Add audio file to backend/audio_files/
   # Update backend/dictionaries/audio_dict.json
   {
     "new_ijaw_translation": "new_ijaw_translation.wav",
     ...
   }
   ```

3. **Restart the backend** to load new translations

### Recording Audio Files

For production use, replace synthetic audio with recordings by native Ijaw speakers:

1. **Record each word** in high quality (44.1kHz, 16-bit WAV)
2. **Name files** according to the audio dictionary
3. **Place files** in `backend/audio_files/`
4. **Update** `backend/dictionaries/audio_dict.json`

## 🔄 Upgrading to Production Models

### Machine Translation Model

Replace dictionary translation with a trained MT model:

```python
# In backend/main.py, replace translate_to_ijaw function
def translate_to_ijaw(english_text: str) -> str:
    # Load your trained model (e.g., Hugging Face Transformers)
    from transformers import pipeline
    translator = pipeline("translation", model="your-en-ijaw-model")
    result = translator(english_text)
    return result[0]['translation_text']
```

### Text-to-Speech Model

Replace audio concatenation with a TTS model:

```python
# In backend/main.py, replace generate_audio_from_text function
def generate_audio_from_text(ijaw_text: str) -> str:
    # Use a TTS model (e.g., Coqui TTS, Tacotron)
    import tts_model
    audio = tts_model.synthesize(ijaw_text, language="ijaw")
    # Save and return filename
    return save_audio(audio)
```

## 🛠️ Development

### Backend Development

- **Add new endpoints** in `backend/main.py`
- **Modify translation logic** in the `translate_to_ijaw` function
- **Improve audio generation** in the `generate_audio_from_text` function
- **Add logging** for debugging and monitoring

### Frontend Development

- **Modify UI** in `frontend/src/App.js`
- **Update styling** in `frontend/src/App.css`
- **Add new features** like translation history, user accounts, etc.
- **Improve error handling** and user feedback

### Testing

```bash
# Backend tests
cd backend
python -m pytest tests/

# Frontend tests
cd frontend
npm test
```

## 🐛 Troubleshooting

### Common Issues

1. **Microphone not working:**
   - Check browser permissions
   - Ensure HTTPS or localhost
   - Try different browsers

2. **Backend connection failed:**
   - Verify backend is running on port 8000
   - Check CORS settings
   - Ensure firewall allows connections

3. **Audio playback issues:**
   - Check browser audio support
   - Verify audio files exist
   - Try different audio formats

4. **Translation quality:**
   - Add more words to dictionary
   - Improve grammar rules
   - Consider using ML models

### Performance Optimization

- **Use smaller Whisper models** for faster transcription
- **Implement caching** for repeated translations
- **Optimize audio file sizes** for faster loading
- **Add request queuing** for high traffic

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
3. **Add your improvements**
4. **Test thoroughly**
5. **Submit a pull request**

### Areas for Contribution

- **Linguistic expertise** for better Ijaw translations
- **Audio recordings** by native speakers
- **UI/UX improvements**
- **Performance optimizations**
- **Additional language pairs**

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Ijaw language community** for linguistic guidance
- **OpenAI Whisper** for speech recognition
- **FastAPI** and **React** communities
- **Contributors** and **testers**

## 📞 Support

For questions, issues, or contributions:
- Create an issue on GitHub
- Contact the development team
- Join our community discussions

---

**Built with ❤️ for Ijaw language preservation and accessibility**#   i t r a n s l a t e  
 