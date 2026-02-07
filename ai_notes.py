from google import genai
import os


def generate_notes_summary(transcript, tone, length):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found.")

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an AI Lecture Notes Generator.

Create structured academic notes from this lecture transcript.

Transcript:
{transcript}

Format:

LECTURE NOTES:
1. Topic Overview
2. Key Concepts
3. Definitions
4. Important Explanations
5. Examples
6. Exam Points
7. Revision Points

SUMMARY:
Tone: {tone}
Length: {length}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text

    if "SUMMARY:" in text:
        notes = text.split("SUMMARY:")[0]
        summary = text.split("SUMMARY:")[1]
    else:
        notes = text
        summary = "Summary not generated."

    return notes, summary
