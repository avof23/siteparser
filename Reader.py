from dataclasses import dataclass

@dataclass
class ReaderFile:
    filename: str
    mode: str = 'r'
    encoding: str = 'utf8'

    def read_from_file(self):
        with open(self.filename, mode=self.mode, encoding=self.encoding) as file_obj:
            content = file_obj.read()
            return content
