import os
from pydub import AudioSegment

def convert_mp3_to_wav(mp3_dir, export_dir):
    # Ensure that the mp3 directory exists
    if not os.path.exists(mp3_dir):
        print(f"The directory {mp3_dir} does not exist.")
        return
    
    # Ensure that the export directory exists; if not, create it
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    
    # Loop through all files in the directory
    for filename in os.listdir(mp3_dir):
        if filename.endswith(".mp3"):
            mp3_path = os.path.join(mp3_dir, filename)
            wav_filename = os.path.splitext(filename)[0] + ".wav"
            wav_path = os.path.join(export_dir, wav_filename)
            
            # Convert mp3 to wav
            try:
                audio = AudioSegment.from_mp3(mp3_path)
                audio.export(wav_path, format="wav")
                print(f"Converted {filename} to {wav_filename}")
            except Exception as e:
                print(f"Failed to convert {filename}: {e}")

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.realpath(__file__))

# Set the relative paths for the directories
mp3_dir = os.path.join(script_dir, "OUTPUT_DUBBING")
export_dir = os.path.join(script_dir, "wavExport")

# Convert the MP3 files to WAV
convert_mp3_to_wav(mp3_dir, export_dir)

# Pause the script so the window doesn't close immediately
input("Press Enter to exit...")
