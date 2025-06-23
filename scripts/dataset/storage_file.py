import pathlib
import os

from dataset.models import Entry
from storage import Storage
from dataset.utils import create_folder
from dataset.logger import logger


class FileSystemStore(Storage):
    data_dir: str = ""

    @property
    def info(self) -> str:
        return f'File System Storage on {self.data_dir}'

    def __init__(self):
        data_dir = os.getenv("DATADIR")
        if data_dir is None:
            raise EnvironmentError("DATADIR environment variable is not set")

        create_folder(pathlib.Path(data_dir))
        self.data_dir = data_dir

    def store(self, document: Entry) -> Entry:
        logger.info(
            f"Storing {document.id} to {self.data_dir}/{document.source}/{document.topic}")
        d = pathlib.Path(f'{self.data_dir}/{document.source}')
        if not d.exists():
            create_folder(d)

        f = pathlib.Path(
            f'{self.data_dir}/{document.source}/{document.topic}.csv')
        if not f.exists():
            f.touch()
        document.stored_at = datetime.datetime.now(
                datetime.UTC).timetuple()
        f.write_text(
            "\n".join(
                sorted(
                    f.read_text().split("\n") + [str(document)]
                )
            )
        )
        return document
