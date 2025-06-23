import os
import sys
import pathlib
import hashlib
from datetime import datetime
from os import PathLike


def create_folder(p: pathlib.Path):
    try:
        p.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        sys.exit(f"Permission denied: Unable to create '{p}'.")
    except Exception as e:
        sys.exit(f"An error occurred: {e}")


def get_hash_hexdigest(s: str) -> str:
    return hashlib.md5(s.encode()).hexdigest()


def get_last_created_data_file_in_dir(p: pathlib.Path) -> None | PathLike:
    files = list(p.glob("*.csv"))
    if not files:
        return None
    return max(files, key=os.path.getctime)

def timetuple_to_datetime(t: datetime.timetuple) -> datetime:
    return datetime(*t[:6])