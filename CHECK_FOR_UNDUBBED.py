import os
import csv
import re

# Define directories relative to the script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
CHECK_FOLDER = os.path.join(script_dir, "ALL_CURRENT_DUBS")
DIALOGUES_CSV = os.path.join(script_dir, "DIALOGUES.csv")
REFERENCE_CSV = os.path.join(script_dir, "REFERENCE.csv")
OUTPUT_CSV = os.path.join(script_dir, "MISSING_SOUNDS_LIST.csv")

def extract_sound_id(ai_output_str):
    """Extracts the sound ID from an AI_OUTPUT string."""
    match = re.search(r'"([^"]+)"', ai_output_str)
    return match.group(1).strip().upper() if match else None

def load_dialogues_csv(csv_file):
    """Reads the DIALOGUES.csv and extracts sound IDs."""
    sound_ids = set()

    with open(csv_file, 'r', encoding='utf-8') as f:
        for line in f:
            fields = line.strip().split('\t')
            if len(fields) == 7 and fields[5].strip().upper() == "SUBTITLE":
                sound_id = extract_sound_id(fields[4])  # Extract from AI_OUTPUT column
                if sound_id:
                    sound_ids.add(sound_id.upper())

    return sound_ids

def load_reference_csv(csv_file):
    """Reads the REFERENCE.csv and extracts sound IDs."""
    sound_ids = set()

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            key_column = row[4]  # The AI_OUTPUT(...) column
            if 'AI_OUTPUT' in key_column:
                start = key_column.find('"') + 1
                end = key_column.rfind('"')
                extracted_key = key_column[start:end].upper()  # Normalize to uppercase
                sound_ids.add(extracted_key)

    return sound_ids

def check_missing_wav_files(sound_ids, check_folder):
    """Checks if corresponding .wav files exist for the sound IDs in the folder."""
    missing_files = []

    for sound_id in sound_ids:
        wav_file_path = os.path.join(check_folder, f"{sound_id}.wav")
        if not os.path.exists(wav_file_path):
            missing_files.append(sound_id)

    return missing_files

def save_missing_files_to_csv(missing_files, output_csv):
    """Saves the missing files list to a CSV file."""
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Sound ID"])  # Header row
        for sound_id in missing_files:
            writer.writerow([sound_id])

def main():
    # Load sound IDs from DIALOGUES.csv and REFERENCE.csv
    dialogues_sound_ids = load_dialogues_csv(DIALOGUES_CSV)
    reference_sound_ids = load_reference_csv(REFERENCE_CSV)

    # Combine both sets of sound IDs
    all_sound_ids = dialogues_sound_ids.union(reference_sound_ids)

    # Check for missing .wav files in CHECK_FOR_UNDUBBED_SPEECH
    missing_files = check_missing_wav_files(all_sound_ids, CHECK_FOLDER)

    # If there are missing files, process them
    if missing_files:
        # Sort the missing files alphabetically
        missing_files.sort()

        # Save the sorted missing files to a CSV file
        save_missing_files_to_csv(missing_files, OUTPUT_CSV)

        # Print the sorted missing files
        print("⚠️ The following sound files are missing:")
        for sound_id in missing_files:
            print(f"  - {sound_id}")
        print(f"\nThe list of missing files has been saved to {OUTPUT_CSV}")
    else:
        print("✅ All sound files are present!")

if __name__ == "__main__":
    main()
