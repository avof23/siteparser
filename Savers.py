from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Saver(ABC):

    filename: str
    content: str
    mode: str = 'w'
    encoding: str = 'utf8'

    @abstractmethod
    def save_to_file(self):
        pass


class SaverJson(Saver):

    def save_to_file(self):
        pass


class SaverText(Saver):

    def save_to_file(self):
        with open(self.filename, mode=self.mode, encoding=self.encoding) as file_obj:
            file_obj.write(self.content)
