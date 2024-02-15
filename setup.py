import os
import subprocess

# Clone the repository
subprocess.run(["git", "clone", "https://github.com/Eddycrack864/Dependencies_en.git"])

# Unzip the required files
subprocess.run(["unzip", "-n", "Dependencies_en/FIX.zip", "-d", "."])

# Change directory
os.chdir('FIX')

# subprocess.run(["pip", "install", "-q", "-r", "requirements.txt"])

# Update system packages
subprocess.run(["sudo", "apt", "update"])

# Install SoX
subprocess.run(["sudo", "apt", "install", "sox", "-y"])

# subprocess.run(["python", "-m", "pip", "install", "ort-nightly-gpu", "--index-url=https://aiinfra.pkgs.visualstudio.com/PublicPackages/_packaging/ort-cuda-12-nightly/pypi/simple/"])

# Download MDXNet Vocal Separation and Hubert Base Models
subprocess.run(["python", "src/download_models.py"])
