import os
import uuid
import logging
from typing import Optional

from gtts import gTTS
from gtts.lang import tts_langs

OUTPUT_DIR = "output_audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

logger = logging.getLogger(__name__)

def synthesize_speech(text: str, lang: Optional[str] = None, slow: bool = False) -> str:
    """Generate an MP3 file using gTTS and return the filename.

    Note: gTTS language support does not currently include Ijaw; by default we
    use English (en) to audibly render the provided text. You can set the
    environment variable TTS_LANG to override the language code.
    """
    if not text:
        text = ""

    tts_lang = (lang or os.getenv("TTS_LANG") or "en").strip()
    supported = tts_langs()
    if tts_lang not in supported:
        fallback_lang = (os.getenv("TTS_FALLBACK_LANG") or "en").strip()
        logger.warning(
            f"Requested TTS language '{tts_lang}' not supported by gTTS. "
            f"Falling back to '{fallback_lang}'."
        )
        tts_lang = fallback_lang

    audio_id = str(uuid.uuid4())[:8]
    filename = f"tts_{tts_lang}_{audio_id}.mp3"
    filepath = os.path.join(OUTPUT_DIR, filename)

    try:
        tts = gTTS(text=text, lang=tts_lang, slow=slow)
        tts.save(filepath)
        logger.info(f"gTTS synthesized MP3: {filename} (lang={tts_lang}, slow={slow})")
        return filename
    except Exception as e:
        logger.error(f"gTTS synthesis failed: {e}")
        raise