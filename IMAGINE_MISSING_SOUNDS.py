import os
import pandas as pd

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the CSV file (assuming it's in the same directory as the script)
csv_file = os.path.join(script_dir, 'MISSING_SOUNDS_LIST.csv')

# Directory where the .wav files will be created
output_dir = os.path.join(script_dir, 'MISSING_SOUNDS')

# Create the MISSING_SOUNDS directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Read the CSV file using pandas
df = pd.read_csv(csv_file)

# Loop through each Sound ID
for sound_id in df['Sound ID']:
    # Create the .wav file name
    wav_filename = f"{sound_id}.wav"
    
    # Construct the full path for the .wav file in the MISSING_SOUNDS directory
    wav_file_path = os.path.join(output_dir, wav_filename)
    
    # Create an empty file (you can add more functionality here if needed)
    with open(wav_file_path, 'w') as file:
        pass  # Currently, the file is empty; you could add content or metadata if required
    
    print(f"Created: {wav_file_path}")

print("All missing sound files have been created.")
