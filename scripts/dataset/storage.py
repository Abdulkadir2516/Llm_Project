from abc import abstractproperty
from typing import Any
from dataset.logger import logger


class Storage:
    @property
    def info(self) -> str:
        return "Base Storage"

    def store(self, document: Any) -> Any:
        raise NotImplementedError()
    
    def ping(self) -> bool:
        return true


class DummyStorage(Storage):
    @property
    def info(self) -> str:
        return "Dummy Storage"

    def store(self, document: Any) -> Any:
        logger.info(f'Document stored: {str(document)}')
        return
