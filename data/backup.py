import glob, os
import shutil
from pathlib import Path

backup_file_types = [".doc",".docx", ".odt", ".pdf", ".xls", 
                    ".xlsx", ".ods", ".ppt", ".pptx", ".txt", 
                    ".jpg", ".jpeg", ".gif", ".png", ".mp3", ".mp4"]


def init_backup_routine(destination, reserved):
    try:
        for filename in glob.iglob(os.environ["systemdrive"] + "/**", recursive=True):
            if os.path.isfile(filename):
                if Path(filename).suffix.lower() in backup_file_types:
                    shutil.copy(filename, destination + "/")
    except Exception as e:
        print(e)
        return
