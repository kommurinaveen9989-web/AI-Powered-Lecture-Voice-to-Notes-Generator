import whisper
import os


def transcribe_audio(audio_path, model_choice="Local Whisper"):

    if not os.path.exists(audio_path):
        raise FileNotFoundError(audio_path)

    model = whisper.load_model("base")

    result = model.transcribe(
        audio_path,
        fp16=False
    )

    transcript = result["text"]
    segments = result.get("segments", [])

    return transcript, segments
