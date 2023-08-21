
from dataclasses import dataclass, field
import re
import time

from bs4 import BeautifulSoup

import savers
from reader import ReaderContent

SITE_URL = "https://servak.com.ua/"
DUMP_FILE = "data/servak_com_ua.json"


@dataclass
class Parser:
    __content: str = None
    parser_result: list[dict[str]] = field(default_factory=list)

    def get_parser_result(self):
        return self.parser_result

    def get_categories(self, url: str, id_category: str = None, id_category_l1: str = None):
        self.identity_category = id_category
        self.identity_category_l1 = id_category_l1
        mainpage = ReaderContent(url)
        self.__content = mainpage.get_from_url()
        # self.__content = mainpage.get_from_file()

        soup = BeautifulSoup(self.__content, 'html.parser')

        categories_ul = soup.find_all("ul", id=self.identity_category)
        categories = categories_ul[0].find_all("a")
        i = -1
        for category in categories:
            try:
                if self.identity_category_l1 in category['class']:
                    self.parser_result.append({'name_l1': category.text.strip(), 'url': category['href'], 'sub_l2': []})
                    i += 1
                else:
                    self.parser_result[i]['sub_l2'].append({'name_l2': category.text.strip(), 'url': category['href']})
            except KeyError:
                self.parser_result.append({'name_l1': category.text.strip(), 'url': category['href']})
                i += 1

    def get_some_products(self, url: str):
        productpage = ReaderContent(url)
        self.__content = productpage.get_from_url()
        # self.__content = productpage.get_from_file()
        soup = BeautifulSoup(self.__content, 'html.parser')
        product_div = soup.find_all("div", class_=self.identity_product)
        list_of_products = list()
        for product in product_div:
            image = product.find("img", class_=self.identity_image)
            imageurl = image['src']
            caption = product.find("div", class_=self.identity_properties)
            producturl = caption.a['href']
            productname = caption.a.text
            if caption.find("p", class_='price'):
                price = caption.find("p", class_='price').text
            else:
                price = "нет в наличии"
            if caption.find("p", class_='description'):
                short_description = caption.find("p", class_='description').text
            else:
                short_description = "..."
            list_properties = [prop.text for prop in caption.find_all("div", re.compile("option"))]

            list_of_products.append({'name_el': productname,
                    'description': short_description,
                    'price': price.strip(),
                    'image': imageurl,
                    'url': producturl,
                    'properties': list_properties})

        return list_of_products

    def get_products_cat(self, id_product: str = None, id_image: str = None, id_properties: str = None):
        self.identity_product = id_product
        self.identity_image = id_image
        self.identity_properties = id_properties

        for element in self.parser_result:
            if 'sub_l2' in element:
                for sub_l2_element in element['sub_l2']:
                    sub_l2_element['elements'] = self.get_some_products(sub_l2_element['url'])
                    time.sleep(180)
            else:
                element['elements'] = self.get_some_products(element['url'])
                time.sleep(180)


# Для уменьшения кол-ва запросов , делаем сохранение в file, затем вычитываем в переменную content для парсинга
# from savers import SaverText
# mainpage = ReaderContent(site_url)
# tofile = SaverText('site_index.html', mainpage.get_from_url())
# tofile.save_to_file()
# SITE_URL = 'site_index.html'


site_pars = Parser()
site_pars.get_categories(SITE_URL, id_category='menu-list', id_category_l1='with-child')
site_pars.get_products_cat(id_product='product-thumb', id_image='img-responsive', id_properties='caption')

tojson = savers.SaverJson(DUMP_FILE, site_pars.get_parser_result())
tojson.save_to_file()
