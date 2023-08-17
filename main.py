
from dataclasses import dataclass

from bs4 import BeautifulSoup
import requests
import urllib3

from Savers import SaverText
from Reader import ReaderFile

urllib3.disable_warnings()
site_url = "https://servak.com.ua/"


@dataclass
class GetterContent:
    base_url: str

    def get_from_url(self):
        r = requests.get(self.base_url, verify=False)
        return r.text


@dataclass
class Parser:
    content: str
    identity_category: str = None
    identity_category_l1: str = None

    def get_categories(self):
        categories_l1 = dict()
        soup = BeautifulSoup(self.content, 'html.parser')
        # Парсинг категорий L1 содержащих вложенные
        #for element in soup.find_all("a", attrs = {"class": self.identity_category}):
        #for element in soup.find_all("a", class_=self.identity_category):
        #for element in soup.css.select(self.identity_category):
        #    print(element.text)
        #    print(element['href'])
        #categories_l1 = [{'name_l1':element.text.strip(), 'url':element['href'], 'sub_l2':[]} for element in soup.find_all("a", attrs = {"class": self.identity_category})]
        #print(categories_l1)

        categories_ul = soup.find_all("ul", id=self.identity_category)
        categories = categories_ul[0].find_all("a")
        parser_result = []
        i = -1
        for category in categories:
            try:
                if self.identity_category_l1 in category['class']:
                    parser_result.append({'name_l1':category.text.strip(), 'url':category['href'], 'sub_l2':[]})
                    i += 1
                else:
                    parser_result[i]['sub_l2'].append({'name_l2': category.text.strip(), 'url': category['href']})
            except KeyError:
                parser_result.append({'name_l1': category.text.strip(), 'url': category['href']})
                i += 1
        print(parser_result)

    def get_products(self):
        pass

# Для уменьшения кол-ва запросов , делаем сохранение в file, затем вычитываем в переменную content для парсинга
# mainpage = GetterContent(site_url)
# tofile = SaverText('site_index.html', mainpage.get_from_url())
# tofile.save_to_file()
fromfile = ReaderFile('site_index.html')
content = fromfile.read_from_file()

site_main_pars = Parser(content, 'menu-list', 'with-child')
# for CSS find use ".with-child"
site_main_pars.get_categories()
