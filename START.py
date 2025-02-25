import os
import uuid
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
import csv

# Set ElevenLabs API Key
ELEVENLABS_API_KEY = "API KEY"

# Initialize ElevenLabs client
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# Function to select a folder (for the case you still want to use folder selection manually)
def select_folder(prompt):
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(title=prompt)

# Function to generate TTS and save it to file using the official docs method
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

def read_and_filter_csv(csv_file):
    """
    Read the CSV file line by line and keep only the rows that:
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
    input_folder = os.path.join(script_dir, "INPUT_DUBBING")
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
        # Create a translation map with keys in uppercase for robust matching
        translation_map = {row["sound_name"].strip().upper(): row["text"].strip() 
                           for _, row in df.iterrows()}
    except Exception as e:
        print(f"⚠️ Error reading CSV file: {e}")
        input("Press Enter to exit...")
        return

    # Process files in the input folder
    for file_name in os.listdir(input_folder):
        # Remove file extension from the name
        name_without_ext = os.path.splitext(file_name)[0].strip()
        lookup_name = name_without_ext.upper()  # Ensure comparison is case-insensitive

        # Apply the filter: if a filter string is provided, only process if it is contained in the name
        if filter_string and filter_string.upper() not in lookup_name:
            print(f"Skipping {file_name} because it does not contain the filter '{filter_string}'.")
            continue

        text = None
        # Look for a CSV key that is a prefix of the lookup name (no extension in CSV)
        for key in translation_map:
            if lookup_name.startswith(key):  # Compare the name without extension
                text = translation_map[key]
                break

        if text:
            output_file = os.path.join(output_folder, f"{name_without_ext}.mp3")  # Save without extension
            if os.path.exists(output_file):
                print(f"⏭️ Skipped: {output_file} (Already exists)")
                continue
                
            elevenlabs_text_to_speech(text, output_file, voice_id="API VOICE ID !!!CHANGE HERE!!!")
        else:
            print(f"⚠️ Warning: No translation found for {name_without_ext}")

    input("\n✅ All tasks completed! Press Enter to exit...")

if __name__ == "__main__":
    main()
