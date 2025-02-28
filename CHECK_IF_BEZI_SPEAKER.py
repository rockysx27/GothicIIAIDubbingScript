import os
import csv
import re
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set relative paths for CSV file and sound directory
CSV_FILE = os.path.join(script_dir, "REFERENCE.csv")
SOUND_DIRECTORY = os.path.join(script_dir, "CHARACTERS", "BEZI")

def extract_ai_output_values(ai_output_str):
    """Extracts the first value (HERO, OTHER, SELF, etc.) and sound ID from AI_OUTPUT(...)"""
    match = re.search(r'AI_OUTPUT\(([^,]+),[^,]+,"([^"]+)"\)', ai_output_str)
    if match:
        first_value = match.group(1).strip().upper()  # SELF, OTHER, HERO, etc.
        sound_id = match.group(2).strip().upper()  # Extracted sound ID
        return first_value, sound_id
    return None, None

def get_wav_filenames(directory):
    """Returns a set of .wav filenames without extensions in the given directory (case insensitive)."""
    try:
        return {os.path.splitext(f)[0].strip().upper() for f in os.listdir(directory) if f.lower().endswith(".wav")}
    except FileNotFoundError:
        print(f"❌ Error: Sound directory '{directory}' not found!")
        return set()

def process_csv(csv_file, sound_files):
    """Reads the CSV and prints sound names where AI_OUTPUT starts with HERO, OTHER, or SELF."""
    if not os.path.exists(csv_file):
        print(f"❌ Error: CSV file '{csv_file}' not found!")
        return

    hero_other_count = 0  # Initialize HERO/OTHER count
    self_count = 0  # Initialize SELF count
    hero_other_sounds = []  # Store HERO/OTHER sound names
    self_sounds = []  # Store SELF sound names

    with open(csv_file, 'r', encoding='utf-8') as f:
        for line in f:
            fields = line.strip().split('\t')
            if len(fields) < 7:
                continue  # Skip malformed lines

            trace_value = fields[4]  # AI_OUTPUT(...) column
            first_value, sound_id = extract_ai_output_values(trace_value)

            if first_value and sound_id:  # Only count valid AI_OUTPUT rows
                # Check if linked to HERO, OTHER, or SELF and the sound_id exists in sound_files
                if first_value in {"HERO", "OTHER"} and sound_id in sound_files:
                    hero_other_count += 1  # Increment HERO/OTHER match count
                    hero_other_sounds.append(sound_id)  # Add to HERO/OTHER list
                elif first_value == "SELF" and sound_id in sound_files:
                    self_count += 1  # Increment SELF match count
                    self_sounds.append(sound_id)  # Add to SELF list

    # Print results and categorized sound names
    print(f"\n✅ Sounds linked to HERO or OTHER: {hero_other_count}")
    print(f"✅ Sounds linked to SELF: {self_count}")
    
    # Print HERO/OTHER sound names
    print("\nSounds linked to HERO or OTHER:")
    for sound in hero_other_sounds:
        print(f"  - {sound}")

    # Print SELF sound names with indentation and color
    print("\nSounds linked to SELF:")
    for sound in self_sounds:
        print(f"    {Fore.RED}- {sound}{Fore.RESET}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_folder = os.path.join(script_dir, SOUND_DIRECTORY)
    output_folder = os.path.join(script_dir, "OUTPUT_DUBBING")

    if not os.path.exists(input_folder) or not os.path.exists(output_folder):
        print("⚠️ Error: One or more required files/folders are missing.")
        input("Press Enter to exit...")
        return

    # Get the sound files from the directory
    sound_files = get_wav_filenames(input_folder)
    total_sounds = len(sound_files)

    # Print total sounds processed (total sounds in the folder)
    print(f"📂 Total sounds in folder: {total_sounds}")

    # Process CSV and count sounds linked to HERO, OTHER, or SELF
    process_csv(CSV_FILE, sound_files)

    input("\n✅ All tasks completed! Press Enter to exit...")

if __name__ == "__main__":
    main()
