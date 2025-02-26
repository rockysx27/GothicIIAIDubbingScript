import sys
import os
import random
import re
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings

# Set ElevenLabs API Key
ELEVENLABS_API_KEY = "API ID"
VOICE_ID_EL = "VOICE ID"
INPUT_DIR = "INPUT_DUBBING/[char name]"

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
    """Reads the CSV file and extracts subtitle text grouped by sound ID,
    including only those with more than one unique translation.
    """
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

    # ✅ Store values as lists instead of joined strings
    return {key: sorted(value) for key, value in translation_map.items() if len(value) > 1}

def reorder_translation_map(translation_map):
    for key, value in translation_map.items():
        if isinstance(value, str):  # Convert to list if mistakenly stored as string
            value = value.split(" ")

        if isinstance(value, list) and len(value) > 1:  # Only reorder if multiple sections exist
            print(f"\nSentence Key: {key}")
            print("Current Sections:")
            
            for i, section in enumerate(value, 1):
                print(f"{i}: {section}")
            
            while True:
                try:
                    new_order = input("Enter new order as space-separated numbers (e.g., '2 1 3'): ").strip()
                    new_order = list(map(int, new_order.split()))

                    if sorted(new_order) != list(range(1, len(value) + 1)):
                        raise ValueError("Invalid input. Ensure all numbers from 1 to the total sections are included.")

                    # Reorder the list based on user input
                    value = [value[i - 1] for i in new_order]

                    # Add a break tag after each section except the last one
                    value_with_breaks = []
                    last_break_time = 0  # Track the previous break time

                    for i, section in enumerate(value):
                        value_with_breaks.append(section)
                        
                        # Calculate the proportion of the section length to total sentence length
                        section_length = len(section)
                        total_length = sum(len(s) for s in value)
                        proportion = section_length / total_length

                        # Randomize the break time
                        random_break_time = random.uniform(0.1, 0.2)

                        # Modify break time based on the section's proportion of total sentence length
                        adjusted_break_time = random_break_time * proportion
                        
                        # Ensure that the break time doesn't get too small (e.g., below 0.1)
                        adjusted_break_time = max(adjusted_break_time, 0.1)

                        # If this is not the last section, add the break time
                        if i < len(value) - 1:
                            value_with_breaks.append(f'<break time="{adjusted_break_time:.1f}s" />')

                        # Store this break time for possible influence on next section
                        last_break_time = adjusted_break_time

                    translation_map[key] = value_with_breaks
                    break
                except ValueError as e:
                    print(f"Error: {e}. Please try again.")

    # ✅ Convert the ordered lists back into space-separated strings (so it works in later parts of your script)
    for key in translation_map:
        if isinstance(translation_map[key], list):
            translation_map[key] = ' '.join(translation_map[key])  

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

    # ✅ Get sound IDs that match files in `input_folder`
    valid_keys = set(
        os.path.splitext(file_name)[0].strip().upper()
        for file_name in os.listdir(input_folder)
        if file_name.lower().endswith(".wav")
    )

    # ✅ Filter translation_map to only keep relevant keys
    translation_map = {key: value for key, value in translation_map.items() if key in valid_keys}

    # Ask for reordering only for relevant translations
    reorder_translation_map(translation_map)

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
