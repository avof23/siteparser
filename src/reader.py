from dataclasses import dataclass

import requests
import urllib3

urllib3.disable_warnings()

@dataclass
class ReaderContent:
    base_url: str
    mode: str = 'r'
    encoding: str = 'utf8'

    def get_from_url(self):
        reader = requests.get(self.base_url, verify=False, timeout=10)
        return reader.text

    def get_from_file(self):
        with open(self.base_url, mode=self.mode, encoding=self.encoding) as file_obj:
            reader = file_obj.read()
            return reader
