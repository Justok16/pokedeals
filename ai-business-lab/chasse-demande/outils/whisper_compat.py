"""Compatibilité faster-whisper (17/11/2026).

La bibliothèque audio « av » 19 a retiré l'option `metadata_errors` que faster-whisper 1.2.1 lui passe :
toute transcription d'un fichier échouait (« open() got an unexpected keyword argument 'metadata_errors' »).
Ce module remplace le décodage de faster-whisper par ffmpeg (fourni par imageio-ffmpeg), sans dépendre d'« av ».
Usage : `import whisper_compat  # noqa: F401` avant `from faster_whisper import WhisperModel`.
"""
import subprocess

import numpy as np


def _decoder(fichier, sampling_rate=16000, split_stereo=False):
    if not isinstance(fichier, str):
        raise TypeError("whisper_compat : chemin de fichier attendu")
    import imageio_ffmpeg

    brut = subprocess.run(
        [imageio_ffmpeg.get_ffmpeg_exe(), "-loglevel", "error", "-i", fichier, "-f", "s16le", "-ac", "1",
         "-ar", str(sampling_rate), "-"],
        capture_output=True, check=True,
    ).stdout
    return np.frombuffer(brut, np.int16).astype(np.float32) / 32768.0


try:
    import faster_whisper.audio as _audio
    import faster_whisper.transcribe as _transcribe

    _audio.decode_audio = _decoder
    _transcribe.decode_audio = _decoder
except ImportError:  # faster-whisper absent : le code appelant gère déjà ce cas
    pass
