import os
import uuid
from pydub import AudioSegment

UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


def save_uploaded_file(uploaded_file):

    filename = str(uuid.uuid4()) + os.path.splitext(uploaded_file.name)[1]
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return path


def save_mic_recorder_audio(wav_data):

    filename = str(uuid.uuid4()) + ".wav"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as f:
        f.write(wav_data)

    return path


def format_timestamps(transcript, segments):

    if not segments:
        return transcript

    text = ""

    for seg in segments:
        start = seg["start"]
        line = seg["text"]
        text += f"[{start:.2f}s] {line}\n"

    return text


def convert_audio(input_path, output_format="wav"):

    output_path = input_path

    if not input_path.endswith(".wav"):

        audio = AudioSegment.from_file(input_path)

        output_path = input_path.replace(
            os.path.splitext(input_path)[1],
            ".wav"
        )

        audio.export(output_path, format="wav")

    return output_path
