# 🚀 Setup Guide - English → Ijaw Audio Translator

This guide will help you set up and run the English to Ijaw Audio Translator on your local machine.

## 📋 Prerequisites

### Required Software

1. **Python 3.8 or higher**
   - Download from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

2. **Node.js 16 or higher**
   - Download from [nodejs.org](https://nodejs.org/)
   - This includes npm (Node Package Manager)

3. **FFmpeg** (for audio processing)
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use `winget install ffmpeg`
   - **macOS**: Install with Homebrew: `brew install ffmpeg`
   - **Linux**: Install with package manager: `sudo apt install ffmpeg` (Ubuntu/Debian)

### System Requirements

- **RAM**: Minimum 4GB (8GB recommended for Whisper model)
- **Storage**: At least 2GB free space
- **Internet**: Required for initial setup and model downloads
- **Microphone**: For audio recording functionality

## 🔧 Installation Steps

### Step 1: Download the Project

```bash
# If you have git installed
git clone <repository-url>
cd itranslate

# Or download and extract the ZIP file
```

### Step 2: Backend Setup

1. **Open terminal/command prompt** and navigate to the backend directory:
   ```bash
   cd backend
   ```

2. **Create a Python virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   This will install:
   - FastAPI (web framework)
   - Whisper (speech recognition)
   - Pydub (audio processing)
   - And other required packages

4. **Generate sample audio files:**
   ```bash
   python generate_sample_audio.py
   ```

5. **Test the backend:**
   ```bash
   python main.py
   ```
   
   You should see:
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000
   INFO:     Whisper model loaded successfully
   ```

### Step 3: Frontend Setup

1. **Open a new terminal** and navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```
   
   This will install:
   - React (UI framework)
   - Axios (HTTP client)
   - And other required packages

3. **Test the frontend:**
   ```bash
   npm start
   ```
   
   The browser should automatically open to `http://localhost:3000`

## 🎯 Quick Start (Windows)

For Windows users, you can use the provided batch script:

1. **Double-click** `start_dev.bat`
2. **Wait** for both servers to start
3. **Open browser** to `http://localhost:3000`

## 🔍 Verification

### Backend Verification

1. **Open browser** to `http://localhost:8000`
2. **You should see:** `{"message": "English to Ijaw Audio Translator API"}`
3. **Check API docs:** `http://localhost:8000/docs`

### Frontend Verification

1. **Open browser** to `http://localhost:3000`
2. **You should see:** The translator interface
3. **Test microphone:** Click "Start Recording" (allow microphone access)

## 🐛 Common Issues and Solutions

### Issue: "Python not found"
**Solution:**
- Ensure Python is installed and added to PATH
- Try `python3` instead of `python`
- Restart terminal after Python installation

### Issue: "pip not found"
**Solution:**
- Python installation should include pip
- Try `python -m pip` instead of `pip`
- Reinstall Python with pip option checked

### Issue: "FFmpeg not found"
**Solution:**
- Install FFmpeg and add to PATH
- Restart terminal after installation
- On Windows, try using Windows Package Manager: `winget install ffmpeg`

### Issue: "Node/npm not found"
**Solution:**
- Install Node.js from official website
- Restart terminal after installation
- Verify with `node --version` and `npm --version`

### Issue: "Microphone access denied"
**Solution:**
- Allow microphone access in browser
- Use HTTPS or localhost (required for microphone API)
- Check browser settings for microphone permissions

### Issue: "CORS errors"
**Solution:**
- Ensure backend is running on port 8000
- Frontend should proxy requests automatically
- Check that both servers are running

### Issue: "Whisper model download fails"
**Solution:**
- Ensure stable internet connection
- Model downloads automatically on first use
- Try smaller model: change `"base"` to `"tiny"` in `main.py`

### Issue: "Audio playback not working"
**Solution:**
- Check browser audio permissions
- Ensure audio files are generated in `backend/audio_files/`
- Try different browser

## 🔧 Advanced Configuration

### Using Different Whisper Models

Edit `backend/main.py` and change the model size:

```python
# Options: tiny, base, small, medium, large
whisper_model = whisper.load_model("tiny")  # Faster, less accurate
whisper_model = whisper.load_model("large") # Slower, more accurate
```

### Customizing Audio Quality

Edit `backend/generate_sample_audio.py` to adjust audio parameters:

```python
# Higher quality audio
final_audio.export(file_path, format="wav", parameters=["-ar", "44100", "-ac", "2"])
```

### Adding HTTPS (for production)

For production deployment, configure HTTPS:

```python
# In main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, ssl_keyfile="key.pem", ssl_certfile="cert.pem")
```

## 📱 Browser Compatibility

### Supported Browsers
- ✅ Chrome 60+
- ✅ Firefox 55+
- ✅ Safari 11+
- ✅ Edge 79+

### Required Features
- Web Audio API
- MediaRecorder API
- Fetch API
- ES6 support

## 🚀 Production Deployment

### Backend Deployment

1. **Use production WSGI server:**
   ```bash
   pip install gunicorn
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

2. **Configure environment variables:**
   ```bash
   export WHISPER_MODEL=base
   export AUDIO_DIR=/path/to/audio/files
   ```

### Frontend Deployment

1. **Build for production:**
   ```bash
   npm run build
   ```

2. **Serve static files:**
   ```bash
   npm install -g serve
   serve -s build
   ```

## 📞 Getting Help

If you encounter issues not covered here:

1. **Check the logs** in terminal for error messages
2. **Verify all prerequisites** are installed correctly
3. **Try the troubleshooting steps** above
4. **Create an issue** on GitHub with:
   - Your operating system
   - Python and Node.js versions
   - Complete error messages
   - Steps to reproduce the issue

## 🎉 Success!

Once everything is running, you should have:

- ✅ Backend API at `http://localhost:8000`
- ✅ Frontend UI at `http://localhost:3000`
- ✅ Working microphone recording
- ✅ English to Ijaw translation
- ✅ Audio playback of Ijaw translations

**Happy translating! 🎤→🌍**