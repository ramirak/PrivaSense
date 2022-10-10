import glob, os
import shutil
from pathlib import Path
import os, uuid
from encryption.encryption_manager import encrypt_folder
import data.enums as enums


def init_backup_routine(sources ,destination, reserved):
    try:
        new_folder_name = uuid.uuid4().hex
        for source in sources:
            shutil.copytree(source, destination + "/" + new_folder_name)
            encrypt_folder(destination, None)
        return enums.results.SUCCESS.value
    except Exception as e:
        return enums.results.ERR_UNKNOWN.value
       
