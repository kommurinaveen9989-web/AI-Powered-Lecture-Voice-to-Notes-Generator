import streamlit as st
from stt import transcribe_audio
from ai_notes import generate_notes_summary
from utils import (
    save_uploaded_file,
    save_mic_recorder_audio,
    format_timestamps,
    convert_audio,
)
from streamlit_mic_recorder import mic_recorder
import os
import time

st.set_page_config(
    page_title="AI Lecture Voice → Notes Generator",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 AI Lecture Voice → Notes Generator")

# Sidebar
st.sidebar.header("Settings")

model_choice = st.sidebar.selectbox(
    "STT Model",
    ["Local Whisper"]
)

summary_tone = st.sidebar.selectbox(
    "Summary Tone",
    ["academic", "concise", "detailed", "bullet-points"]
)

summary_length = st.sidebar.selectbox(
    "Summary Length",
    ["short", "medium", "long"]
)

delete_after = st.sidebar.checkbox(
    "Delete audio after processing",
    value=True
)

# ---------------- PROCESS FUNCTION ---------------- #

def process_audio(file_path, key):

    st.audio(file_path)

    converted_path = None
    transcript_text = ""

    with st.spinner("Transcribing lecture audio..."):
        try:
            converted_path = convert_audio(file_path)

            transcript, segments = transcribe_audio(
                converted_path,
                model_choice
            )

            transcript_text = format_timestamps(
                transcript,
                segments
            )

            st.success("Transcription completed!")

        except Exception as e:
            st.error(f"Error: {e}")
            transcript_text = str(e)
            converted_path = file_path

    edited_transcript = st.text_area(
        "Transcript",
        value=transcript_text,
        height=300,
        key=f"text_{key}"
    )

    if st.button("Generate Lecture Notes", key=f"btn_{key}"):

        with st.spinner("Generating notes..."):

            try:
                notes, summary = generate_notes_summary(
                    edited_transcript,
                    summary_tone,
                    summary_length
                )

                st.markdown("## Lecture Notes")
                st.markdown(notes)

                st.download_button(
                    "Download Notes",
                    notes,
                    file_name="lecture_notes.txt"
                )

                st.markdown("## Summary")
                st.write(summary)

                st.download_button(
                    "Download Summary",
                    summary,
                    file_name="lecture_summary.txt"
                )

            except Exception as e:
                st.error(f"Generation failed: {e}")

    # Cleanup
    if delete_after:
        if os.path.exists(file_path):
            os.remove(file_path)
        if converted_path and os.path.exists(converted_path):
            os.remove(converted_path)

# ---------------- LIVE RECORDING ---------------- #

st.markdown("### Record Lecture Live")

audio_output = mic_recorder(
    start_prompt="Start Recording",
    stop_prompt="Stop Recording",
    format="wav",
    key="recorder"
)

if audio_output and "bytes" in audio_output:

    wav_data = audio_output["bytes"]

    if wav_data:
        temp_path = save_mic_recorder_audio(wav_data)
        time.sleep(1)
        process_audio(temp_path, "live")

# ---------------- FILE UPLOAD ---------------- #

st.markdown("### Upload Lecture Audio")

uploaded_files = st.file_uploader(
    "Upload audio",
    type=["wav", "mp3", "m4a", "ogg", "flac"],
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        path = save_uploaded_file(file)
        process_audio(path, file.name)
        break
