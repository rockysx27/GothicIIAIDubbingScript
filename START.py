import os
import re
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings

# Set ElevenLabs API Key
ELEVENLABS_API_KEY = "API KEY"
VOICE_ID = "VOICE ID"
# Initialize ElevenLabs client
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def elevenlabs_text_to_speech(text, output_path, voice_id):
    try:
        response = client.text_to_speech.convert(
            voice_id=voice_id,
            output_format="mp3_22050_32",
            text=text,
            model_id="eleven_turbo_v2_5",  # Using the turbo model for low latency
            voice_settings=VoiceSettings(
                stability=0.0,
                similarity_boost=1.0,
                style=0.0,
                use_speaker_boost=True,
            ),
        )
        with open(output_path, "wb") as f:
            for chunk in response:
                if chunk:
                    f.write(chunk)
        print(f"Generated: {output_path}")
    except Exception as e:
        print(f"❌ Failed to generate audio: {e}")

def extract_sound_id(ai_output_str):
    """Extracts the sound ID from an AI_OUTPUT string."""
    match = re.search(r'"([^"]+)"', ai_output_str)
    return match.group(1).strip().upper() if match else None

def read_and_filter_csv(csv_file):
    """Reads the CSV file and extracts subtitle text grouped by sound ID."""
    translation_map = {}

    with open(csv_file, 'r', encoding='utf-8') as f:
        for line in f:
            fields = line.strip().split('\t')
            if len(fields) == 7 and fields[5].strip().upper() == "SUBTITLE":
                sound_id = extract_sound_id(fields[4])  # Extract from AI_OUTPUT column
                text = fields[6].strip()  # Subtitle text

                if sound_id:
                    if sound_id not in translation_map:
                        translation_map[sound_id] = set()  # Use a set to prevent duplicates
                    translation_map[sound_id].add(text)

    # Convert sets to concatenated strings
    return {key: ' '.join(sorted(value)) for key, value in translation_map.items()}

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_folder = os.path.join(script_dir, "CHARACTERS/MUD")
    output_folder = os.path.join(script_dir, "OUTPUT_DUBBING")
    csv_file = os.path.join(script_dir, "DIALOGUES.csv")

    if not os.path.exists(input_folder) or not os.path.exists(output_folder) or not os.path.exists(csv_file):
        print("⚠️ Error: One or more required files/folders are missing.")
        input("Press Enter to exit...")
        return

    # Read and process the CSV file
    translation_map = read_and_filter_csv(csv_file)

    # Process files in the input folder
    for file_name in os.listdir(input_folder):
        if not file_name.lower().endswith(".wav"):
            continue

        name_without_ext = os.path.splitext(file_name)[0].strip().upper()

        if name_without_ext in translation_map:
            text = translation_map[name_without_ext]
            output_file = os.path.join(output_folder, f"{name_without_ext}.mp3")

            if os.path.exists(output_file):
                print(f"⏭️ Skipped: {output_file} (Already exists)")
                continue

            elevenlabs_text_to_speech(text, output_file, voice_id=VOICE_ID)
        else:
            print(f"⚠️ Warning: No translation found for {name_without_ext}")

    input("\n✅ All tasks completed! Press Enter to exit...")

if __name__ == "__main__":
    main()
