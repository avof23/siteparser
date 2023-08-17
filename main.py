
from dataclasses import dataclass, field

from bs4 import BeautifulSoup

from savers import SaverText
from reader import ReaderContent

SITE_URL = "https://servak.com.ua/"

@dataclass
class Parser:
    __content: str = None
    parser_result: list[dict[str]] = field(default_factory=list)

    def get_categories(self, url: str, id_category: str = None, id_category_l1: str = None):
        self.identity_category = id_category
        self.identity_category_l1 = id_category_l1
        mainpage = ReaderContent(url)
        #self.__content = mainpage.get_from_url()
        self.__content = mainpage.get_from_file()

        soup = BeautifulSoup(self.__content, 'html.parser')

        categories_ul = soup.find_all("ul", id=self.identity_category)
        categories = categories_ul[0].find_all("a")
        i = -1
        for category in categories:
            try:
                if self.identity_category_l1 in category['class']:
                    self.parser_result.append({'name_l1':category.text.strip(), 'url':category['href'], 'sub_l2':[]})
                    i += 1
                else:
                    self.parser_result[i]['sub_l2'].append({'name_l2': category.text.strip(), 'url': category['href']})
            except KeyError:
                self.parser_result.append({'name_l1': category.text.strip(), 'url': category['href']})
                i += 1
        print(self.parser_result)

    def get_products(self, id_product: str = None, id_image: str = None, id_properties: str = None):
        self.identity_product = id_product
        self.identity_image = id_image
        self.identity_properties = id_properties

        productpage = ReaderContent(None)
        # self.__content = productpage.get_from_url()
        self.__content = productpage.get_from_file()


# Для уменьшения кол-ва запросов , делаем сохранение в file, затем вычитываем в переменную content для парсинга
# mainpage = ReaderContent(site_url)
# tofile = SaverText('site_index.html', mainpage.get_from_url())
# tofile.save_to_file()
SITE_URL = 'site_index.html'

# Выборка категорий товаров с главной страницы
site_pars = Parser()
site_pars.get_categories(SITE_URL, id_category='menu-list', id_category_l1='with-child')
site_pars.get_products(id_product='product-thumb', id_image='image', id_properties='caption')
