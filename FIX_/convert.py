import os
import zipfile
import shutil
import urllib.request

# Define base directory and model directory
BASE_DIR = os.getcwd()
if not BASE_DIR.endswith('FIX'):
    os.chdir('FIX')
    BASE_DIR = os.getcwd()
rvc_models_dir = os.path.join(BASE_DIR, 'rvc_models')

def extract_zip(extraction_folder, zip_name):
    """
    Extracts a zip file to the specified folder and cleans up unnecessary nested folders.
    """
    os.makedirs(extraction_folder, exist_ok=True)
    with zipfile.ZipFile(zip_name, 'r') as zip_ref:
        zip_ref.extractall(extraction_folder)
    os.remove(zip_name)

    index_filepath, model_filepath = None, None
    for root, dirs, files in os.walk(extraction_folder):
        for name in files:
            if name.endswith('.index') and os.stat(os.path.join(root, name)).st_size > 1024 * 100:
                index_filepath = os.path.join(root, name)
            if name.endswith('.pth') and os.stat(os.path.join(root, name)).st_size > 1024 * 1024 * 40:
                model_filepath = os.path.join(root, name)

    if not model_filepath:
        raise Exception(f'No .pth model file was found in the extracted zip. Please check {extraction_folder}.')

    os.rename(model_filepath, os.path.join(extraction_folder, os.path.basename(model_filepath)))
    if index_filepath:
        os.rename(index_filepath, os.path.join(extraction_folder, os.path.basename(index_filepath)))

    for filepath in os.listdir(extraction_folder):
        if os.path.isdir(os.path.join(extraction_folder, filepath)):
            shutil.rmtree(os.path.join(extraction_folder, filepath))

def download_model(url, dir_name):
    """
    Downloads and extracts a model from a URL into a specified directory.
    """
    try:
        extraction_folder = os.path.join(rvc_models_dir, dir_name)
        if not os.path.exists(extraction_folder):
            print(f'[~] Downloading voice model with name {dir_name}...')
            zip_name = url.split('/')[-1]
            urllib.request.urlretrieve(url, zip_name)
            print('[~] Extracting zip...')
            extract_zip(extraction_folder, zip_name)
            print(f'[+] {dir_name} Model successfully downloaded!')
        else:
            print(f'[~] Voice model directory {dir_name} already exists! Skipping download...')
    except Exception as e:
        raise Exception(str(e))

# Model Download - Update this section with your model URL and directory name
url = "https://huggingface.co/Eddycrack864/Lana-Rhoades-AI-Voice/resolve/main/lanarhoades.zip?download=true"
dir_name = "LanaRhoades"

if 'drive.google.com' in url:
    print('Google Drive link detected. Manual intervention required for download.')
elif 'huggingface.co' in url:
    download_model(url, dir_name)
else:
    print('Unrecognized URL. Make sure you provide a valid link.')

# Generate Cover - Update this section with your own parameters
import subprocess
import time

SONG_INPUT = "song_output/suAR1PYFNYA/Dua Lipa - Houdini (Official Music Video)_Vocals.wav"
# SONG_INPUT = "https://youtu.be/suAR1PYFNYA?si=ZBXWC6v58xYi-4UX"
RVC_DIRNAME = "LanaRhoades"
PITCH_CHANGE = 0
PITCH_CHANGE_ALL = 0
INDEX_RATE = 0.75
FILTER_RADIUS = 3
PITCH_DETECTION_ALGO = "rmvpe"
CREPE_HOP_LENGTH = 64
PROTECT = 0.33
REMIX_MIX_RATE = 0.25
MAIN_VOL = 0
BACKUP_VOL = 0
INST_VOL = 0
REVERB_SIZE = 0.15
REVERB_WETNESS = 0.2
REVERB_DRYNESS = 0.8
REVERB_DAMPING = 0.7
OUTPUT_FORMAT = "wav"

command = [
    "python", "src/main.py",
    "-i", SONG_INPUT,
    "-dir", RVC_DIRNAME,
    "-p", str(PITCH_CHANGE),
    "-k",
    "-ir", str(INDEX_RATE),
    "-fr", str(FILTER_RADIUS),
    "-rms", str(REMIX_MIX_RATE),
    "-palgo", PITCH_DETECTION_ALGO,
    "-hop", str(CREPE_HOP_LENGTH),
    "-pro", str(PROTECT),
    "-mv", str(MAIN_VOL),
    "-bv", str(BACKUP_VOL),
    "-iv", str(INST_VOL),
    "-pall", str(PITCH_CHANGE_ALL),
    "-rsize", str(REVERB_SIZE),
    "-rwet", str(REVERB_WETNESS),
    "-rdry", str(REVERB_DRYNESS),
    "-rdamp", str(REVERB_DAMPING),
    "-oformat", OUTPUT_FORMAT
]
t = time.time()
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
for line in process.stdout:
    print(line, end='')
process.wait()
print(f'Execution time: {time.time() - t:.2f}s')