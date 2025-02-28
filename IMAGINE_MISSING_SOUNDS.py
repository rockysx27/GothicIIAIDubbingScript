import os
import pandas as pd
import re

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the CSV file (assuming it's in the same directory as the script)
csv_file = os.path.join(script_dir, 'MISSING_FILES.csv')

# Directory where the .wav files will be created
output_dir = os.path.join(script_dir, 'MISSING_SOUNDS')

# Create the MISSING_SOUNDS directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Read the CSV file using pandas
df = pd.read_csv(csv_file)

# Loop through each Sound ID
for sound_id in df['Sound ID']:
    # Strip any leading/trailing whitespace
    sound_id = sound_id.strip()
    
    # Sanitize the sound_id to remove any invalid characters for filenames
    sanitized_sound_id = re.sub(r'[\\/*?:"<>|]', "", sound_id)
    
    # Create the .wav file name
    wav_filename = f"{sanitized_sound_id}.wav"
    
    # Construct the full path for the .wav file in the MISSING_SOUNDS directory
    wav_file_path = os.path.join(output_dir, wav_filename)
    
    try:
        # Create an empty .wav file (you can add content or metadata if needed)
        with open(wav_file_path, 'w') as file:
            pass  # Currently, the file is empty; you could add content if required
        
        print(f"Created: {wav_file_path}")
    except Exception as e:
        print(f"Error creating {wav_file_path}: {e}")

print("All missing sound files have been created.")
