import os
import re
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
import csv

# Set ElevenLabs API Key
ELEVENLABS_API_KEY = "API KEY"
VOICE_ID = "VOICE KEY"

# Initialize ElevenLabs client
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def select_folder(prompt):
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(title=prompt)

def elevenlabs_text_to_speech(text, output_path, voice_id):
    try:
        response = client.text_to_speech.convert(
            voice_id=voice_id,
            output_format="mp3_22050_32",
            text=text,
            model_id="eleven_turbo_v2_5",  # using the turbo model for low latency
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
    """
    Extracts the sound ID from an AI_OUTPUT string.
    Example: Given 'AI_OUTPUT(OTHER,SELF,"NON_5021_Kurt_night3_06")'
    it returns 'NON_5021_Kurt_night3_06' as the sound ID.
    """
    match = re.search(r'"([^"]+)"', ai_output_str)
    if match:
        return match.group(1).strip().upper()
    return None

def read_and_filter_csv(csv_file):
    """
    Reads the CSV file line by line and keeps only rows that:
      - Split into exactly 7 fields (tab-delimited)
      - Have the 6th column equal to "SUBTITLE" (case-insensitive)
    """
    filtered_rows = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        for line in f:
            fields = line.strip().split('\t')
            if len(fields) == 7 and fields[5].strip().upper() == "SUBTITLE":
                filtered_rows.append(fields)
    return filtered_rows

# Main function
def main():
    # Set directories relative to the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_folder = os.path.join(script_dir, "CHARACTERS/KURT")
    output_folder = os.path.join(script_dir, "OUTPUT_DUBBING")
    csv_file = os.path.join(script_dir, "DIALOGUES.csv")
    
    # Ask for the filter string (optional)
    filter_string = input("🔍 Enter filter string (only process files whose names contain this string; leave blank for all): ").strip()

    if not os.path.exists(input_folder) or not os.path.exists(output_folder) or not os.path.exists(csv_file):
        print("⚠️ Error: One or more required files/folders are missing.")
        input("Press Enter to exit...")
        return

    # Read and filter CSV file
    try:
        rows = read_and_filter_csv(csv_file)
        if not rows:
            raise ValueError("No valid rows found in CSV file with the correct format and 'SUBTITLE' type.")
        df = pd.DataFrame(rows, columns=["col1", "col2", "col3", "sound_name", "ai_output", "type", "text"])
        # Create a translation map using the sound ID extracted from the AI_OUTPUT field
        translation_map = {}
        for _, row in df.iterrows():
            sound_id = extract_sound_id(row["ai_output"])
            if sound_id:
                if sound_id not in translation_map:
                    translation_map[sound_id] = []
                translation_map[sound_id].append(row["text"].strip())
    except Exception as e:
        print(f"⚠️ Error reading CSV file: {e}")
        input("Press Enter to exit...")
        return

    # Process files in the input folder
    for file_name in os.listdir(input_folder):
        # Only process .wav files
        if not file_name.lower().endswith(".wav"):
            continue

        # Remove file extension and normalize name
        name_without_ext = os.path.splitext(file_name)[0].strip()
        lookup_name = name_without_ext.upper()

        # Apply filter if provided
        if filter_string and filter_string.upper() not in lookup_name:
            print(f"Skipping {file_name} because it does not contain the filter '{filter_string}'.")
            continue

        text = None
        # Attempt to find an exact match for the sound ID
        if lookup_name in translation_map:
            text = ' '.join(translation_map[lookup_name])  # Join multiple lines into a single text block
        else:
            # Optionally, try a more flexible match if needed
            for key in translation_map:
                if lookup_name.startswith(key):
                    text = ' '.join(translation_map[key])
                    break

        if text:
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
