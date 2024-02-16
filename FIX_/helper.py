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