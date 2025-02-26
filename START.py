import sys
import os
import random
import re
import csv
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings

# Set ElevenLabs API Key
ELEVENLABS_API_KEY = "API ID"
VOICE_ID_EL = "VOICE ID"
INPUT_DIR = "YOUR EXTRACTED FOLDER WITH UNTRANSLATED .WAV SOUNDS for a character, for examples 'INPUT_DUBBING/CHARACTER/BEZI"

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
                stability=0.43,
                similarity_boost=0.77,
                style=0.0,
                use_speaker_boost=True,
                speed=0.93,
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

# Step 1: Read the REFERENCE.CSV and create a mapping of keys to subtitles.
def load_reference_csv(reference_file):
    reference_map = {}
    with open(reference_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            key_column = row[4]  # The AI_OUTPUT(...) column
            subtitle = row[6]  # The subtitle text
            
            # Extract the actual key from AI_OUTPUT format
            if 'AI_OUTPUT' in key_column:
                start = key_column.find('"') + 1
                end = key_column.rfind('"')
                extracted_key = key_column[start:end]  # Extract key inside quotes
                
                # Normalize to uppercase to ensure case-insensitive matching
                reference_map[extracted_key.upper()] = subtitle

    return reference_map

# Step 2: The function that reorders and processes translation_map.
def reorder_translation_map(translation_map, reference_map):
    for key, value in translation_map.items():
        normalized_key = key.upper()  # Normalize to uppercase for matching

        if isinstance(value, str):  # Convert to list if mistakenly stored as string
            value = value.split(" ")

        if isinstance(value, list) and len(value) > 1:  # Only reorder if multiple sections exist
            print(f"\nSentence Key: {key}")
            print("Current Sections:")

            for i, section in enumerate(value, 1):
                print(f"{i}: {section}")

            # Check if the normalized key exists in the reference_map
            if normalized_key in reference_map:
                subtitle = reference_map[normalized_key]  # Get the correct subtitle
                print(f"✅ Found subtitle from REFERENCE.CSV: {subtitle}")

                # Replace the value in translation_map with the correct subtitle
                translation_map[key] = subtitle
            else:
                print(f"⚠️ No subtitle found in REFERENCE.CSV for key {key}")

    print("\n✅ Translation map updated successfully!")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_folder = os.path.join(script_dir, INPUT_DIR)
    output_folder = os.path.join(script_dir, "OUTPUT_DUBBING")
    csv_file = os.path.join(script_dir, "DIALOGUES.csv")
    
    

    if not os.path.exists(input_folder) or not os.path.exists(output_folder) or not os.path.exists(csv_file):
        print("⚠️ Error: One or more required files/folders are missing.")
        input("Press Enter to exit...")
        return

    # Read and process the CSV file
    translation_map = read_and_filter_csv(csv_file)
    reference_map = load_reference_csv(os.path.join(script_dir,'REFERENCE.csv'))

    # ✅ Get sound IDs that match files in `input_folder`
    valid_keys = set(
        os.path.splitext(file_name)[0].strip().upper()
        for file_name in os.listdir(input_folder)
        if file_name.lower().endswith(".wav")
    )

    # ✅ Filter translation_map to only keep relevant keys
    translation_map = {key: value for key, value in translation_map.items() if key in valid_keys}

    # Ask for reordering only for relevant translations
    reorder_translation_map(translation_map, reference_map)

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

            elevenlabs_text_to_speech(text, output_file, voice_id=VOICE_ID_EL)
        else:
            print(f"⚠️ Warning: No translation found for {name_without_ext}")

    input("\n✅ All tasks completed! Press Enter to exit...")

if __name__ == "__main__":
    main()
