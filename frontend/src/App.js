import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const App = () => {
  // State management
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [translationResult, setTranslationResult] = useState(null);
  const [error, setError] = useState(null);
  const [recordingTime, setRecordingTime] = useState(0);

  // Refs
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const recordingIntervalRef = useRef(null);
  const audioPlayerRef = useRef(null);

  // API base URL
  // Prefer env-configured base URL; fall back to proxy/relative
  const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || '';

  // Convert audio blob to WAV format
  const convertToWav = async (audioBlob) => {
    try {
      const arrayBuffer = await audioBlob.arrayBuffer();
      const audioContext = new (window.AudioContext || window.webkitAudioContext)();
      const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
      
      // Convert to WAV
      const wavBuffer = audioBufferToWav(audioBuffer);
      return new Blob([wavBuffer], { type: 'audio/wav' });
    } catch (error) {
      console.error('Error converting audio to WAV:', error);
      // Return original blob if conversion fails
      return audioBlob;
    }
  };

  // Convert AudioBuffer to WAV format
  const audioBufferToWav = (buffer) => {
    const length = buffer.length;
    const numberOfChannels = buffer.numberOfChannels;
    const sampleRate = buffer.sampleRate;
    const arrayBuffer = new ArrayBuffer(44 + length * numberOfChannels * 2);
    const view = new DataView(arrayBuffer);
    
    // WAV header
    const writeString = (offset, string) => {
      for (let i = 0; i < string.length; i++) {
        view.setUint8(offset + i, string.charCodeAt(i));
      }
    };
    
    writeString(0, 'RIFF');
    view.setUint32(4, 36 + length * numberOfChannels * 2, true);
    writeString(8, 'WAVE');
    writeString(12, 'fmt ');
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true);
    view.setUint16(22, numberOfChannels, true);
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, sampleRate * numberOfChannels * 2, true);
    view.setUint16(32, numberOfChannels * 2, true);
    view.setUint16(34, 16, true);
    writeString(36, 'data');
    view.setUint32(40, length * numberOfChannels * 2, true);
    
    // Convert audio data
    let offset = 44;
    for (let i = 0; i < length; i++) {
      for (let channel = 0; channel < numberOfChannels; channel++) {
        const sample = Math.max(-1, Math.min(1, buffer.getChannelData(channel)[i]));
        view.setInt16(offset, sample < 0 ? sample * 0x8000 : sample * 0x7FFF, true);
        offset += 2;
      }
    }
    
    return arrayBuffer;
  };

  // Initialize media recorder
  const initializeMediaRecorder = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          sampleRate: 44100
        } 
      });
      
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm;codecs=opus'
      });
      
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };
      
      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { 
          type: 'audio/webm;codecs=opus' 
        });
        setAudioBlob(audioBlob);
        audioChunksRef.current = [];
        
        // Stop all tracks to release microphone
        stream.getTracks().forEach(track => track.stop());
      };
      
      mediaRecorderRef.current = mediaRecorder;
      return true;
    } catch (error) {
      console.error('Error accessing microphone:', error);
      setError('Could not access microphone. Please check permissions.');
      return false;
    }
  };

  // Start recording
  const startRecording = async () => {
    setError(null);
    setTranslationResult(null);
    setAudioBlob(null);
    
    const initialized = await initializeMediaRecorder();
    if (!initialized) return;
    
    try {
      mediaRecorderRef.current.start();
      setIsRecording(true);
      setRecordingTime(0);
      
      // Start recording timer
      recordingIntervalRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);
      
    } catch (error) {
      console.error('Error starting recording:', error);
      setError('Failed to start recording.');
    }
  };

  // Stop recording
  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      
      // Clear recording timer
      if (recordingIntervalRef.current) {
        clearInterval(recordingIntervalRef.current);
        recordingIntervalRef.current = null;
      }
    }
  };

  // Upload and translate audio
  const translateAudio = async () => {
    if (!audioBlob) {
      setError('No audio recorded. Please record audio first.');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // Convert audio to WAV format for backend compatibility
      const wavBlob = await convertToWav(audioBlob);
      
      const formData = new FormData();
      formData.append('audio_file', wavBlob, 'recording.wav');

      const response = await axios.post(`${API_BASE_URL}/translate`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 30000, // 30 second timeout
      });

      setTranslationResult(response.data);
    } catch (error) {
      console.error('Translation error:', error);
      if (error.response) {
        setError(`Translation failed: ${error.response.data.detail || error.response.statusText}`);
      } else if (error.request) {
        setError('Could not connect to translation server. Please check if the backend is running.');
      } else {
        setError('An unexpected error occurred during translation.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Play translated audio
  const playTranslatedAudio = () => {
    if (translationResult && translationResult.audio_filename) {
      const audioUrl = `${API_BASE_URL}/audio/${translationResult.audio_filename}`;
      
      if (audioPlayerRef.current) {
        audioPlayerRef.current.src = audioUrl;
        audioPlayerRef.current.play().catch(error => {
          console.error('Error playing audio:', error);
          setError('Could not play translated audio.');
        });
      }
    }
  };

  // Format recording time
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  // Clear all data
  const clearAll = () => {
    setAudioBlob(null);
    setTranslationResult(null);
    setError(null);
    setRecordingTime(0);
  };

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (recordingIntervalRef.current) {
        clearInterval(recordingIntervalRef.current);
      }
    };
  }, []);

  return (
    <div className="app">
      <header className="app-header">
        <h1>🎤 English → Ijaw Audio Translator</h1>
        <p>Record English speech and get Ijaw translation with audio</p>
      </header>

      <main className="app-main">
        {/* Recording Section */}
        <section className="recording-section">
          <h2>📹 Record Your Voice</h2>
          
          <div className="recording-controls">
            {!isRecording ? (
              <button 
                className="record-btn start"
                onClick={startRecording}
                disabled={isLoading}
              >
                🎤 Start Recording
              </button>
            ) : (
              <button 
                className="record-btn stop"
                onClick={stopRecording}
              >
                ⏹️ Stop Recording
              </button>
            )}
            
            {audioBlob && (
              <button 
                className="clear-btn"
                onClick={clearAll}
                disabled={isLoading}
              >
                🗑️ Clear
              </button>
            )}
          </div>

          {isRecording && (
            <div className="recording-indicator">
              <div className="recording-pulse"></div>
              <span>Recording... {formatTime(recordingTime)}</span>
            </div>
          )}

          {audioBlob && !isRecording && (
            <div className="recording-status">
              ✅ Audio recorded ({formatTime(recordingTime)})
            </div>
          )}
        </section>

        {/* Translation Section */}
        <section className="translation-section">
          <h2>🔄 Translate to Ijaw</h2>
          
          <button 
            className="translate-btn"
            onClick={translateAudio}
            disabled={!audioBlob || isLoading}
          >
            {isLoading ? '⏳ Translating...' : '🔄 Translate'}
          </button>

          {isLoading && (
            <div className="loading-indicator">
              <div className="spinner"></div>
              <p>Processing your audio... This may take a few moments.</p>
            </div>
          )}
        </section>

        {/* Results Section */}
        {translationResult && (
          <section className="results-section">
            <h2>📝 Translation Results</h2>
            
            <div className="result-card">
              <div className="result-item">
                <h3>🇺🇸 English (Transcribed)</h3>
                <p className="english-text">{translationResult.english_text}</p>
              </div>
              
              <div className="result-item">
                <h3>🌍 Ijaw Translation</h3>
                <p className="ijaw-text">{translationResult.ijaw_text}</p>
              </div>
              
              <div className="result-item">
                <h3>🔊 Ijaw Audio</h3>
                <div className="audio-controls">
                  <button 
                    className="play-btn"
                    onClick={playTranslatedAudio}
                  >
                    ▶️ Play Ijaw Audio
                  </button>
                  
                  <audio 
                    ref={audioPlayerRef}
                    controls
                    className="audio-player"
                  >
                    Your browser does not support the audio element.
                  </audio>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* Error Section */}
        {error && (
          <section className="error-section">
            <div className="error-message">
              ⚠️ {error}
            </div>
          </section>
        )}

        {/* Instructions */}
        <section className="instructions-section">
          <h2>📋 How to Use</h2>
          <ol>
            <li>Click "Start Recording" and speak in English</li>
            <li>Click "Stop Recording" when finished</li>
            <li>Click "Translate" to convert to Ijaw</li>
            <li>Listen to the Ijaw pronunciation</li>
          </ol>
          
          <div className="tips">
            <h3>💡 Tips for Best Results</h3>
            <ul>
              <li>Speak clearly and at a moderate pace</li>
              <li>Use simple, common words when possible</li>
              <li>Ensure good microphone quality</li>
              <li>Keep recordings under 30 seconds for faster processing</li>
            </ul>
          </div>
        </section>
      </main>

      <footer className="app-footer">
        <p>Built with ❤️ for Ijaw language preservation</p>
        <p>This is a prototype - translations may not be perfect</p>
      </footer>
    </div>
  );
};

export default App;