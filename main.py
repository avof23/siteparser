
from dataclasses import dataclass

# from bs4 import BeautifulSoup
import requests
import urllib3

from Savers import SaverText

urllib3.disable_warnings()
site_url = "https://servak.com.ua/"


@dataclass
class GetterContent:
    base_url: str

    def get_from_url(self):
        r = requests.get(self.base_url, verify=False)
        # print(r.status_code)
        return r.text


@dataclass
class Parser:
    category_id: str = None

    def get_categories(self):
        pass
        # soup = BeautifulSoup(r, 'html.parser')
        # print(soup.prettify())

    def get_products(self):
        pass


mainpage = GetterContent(site_url)
tofile = SaverText('site_index.html', mainpage.get_from_url())
tofile.save_to_file()
