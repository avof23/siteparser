import json
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Saver(ABC):
    filename: str
    content: list
    mode: str = 'w'
    encoding: str = 'utf8'

    @abstractmethod
    def save_to_file(self):
        pass


class SaverJson(Saver):

    def save_to_file(self):
        with open(self.filename, mode=self.mode, encoding=self.encoding) as file_obj:
            json.dump(self.content, file_obj, ensure_ascii=False, indent=4, sort_keys=True)


class SaverText(Saver):
    content: str

    def save_to_file(self):
        with open(self.filename, mode=self.mode, encoding=self.encoding) as file_obj:
            file_obj.write(self.content)
