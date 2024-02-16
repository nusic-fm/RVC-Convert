import os
from flask import Flask
import subprocess
import time
from flask_cors import CORS

from FIX_.helper import download_model


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def entry_route():
    return "saulgoodman...", 200

@app.route("/voice-cover", methods=["POST"])
def voice_cover():
    # SONG_INPUT = "song_output/suAR1PYFNYA/Dua Lipa - Houdini (Official Music Video)_Vocals.wav"
    SONG_INPUT = "https://youtu.be/suAR1PYFNYA?si=ZBXWC6v58xYi-4UX"
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
    return "Successful"

if __name__ == "__main__":
    # Model Download - Update this section with your model URL and directory name
    url = "https://huggingface.co/Eddycrack864/Lana-Rhoades-AI-Voice/resolve/main/lanarhoades.zip?download=true"
    dir_name = "LanaRhoades"

    if 'drive.google.com' in url:
        print('Google Drive link detected. Manual intervention required for download.')
    elif 'huggingface.co' in url:
        download_model(url, dir_name)
    else:
        print('Unrecognized URL. Make sure you provide a valid link.')

    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8081)))