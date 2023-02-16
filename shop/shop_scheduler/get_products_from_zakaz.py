import requests
import json
from bs4 import BeautifulSoup

from shop.models import Product
from shop.shop_scheduler.config import *
from shop.shop_scheduler.get_json import get_file, headers


def getCountry(country):
    if not country:
        return '-'
    return country


def insert_into_table(name, slug, old_price, new_price, picture, discount, date, category, country, shop_name):
    product = Product.objects.create(
        name=name,
        slug_nam=slug,
        old_price=old_price,
        new_price=new_price,
        picture=picture,
        percent_of_sale=discount,
        date_of_end=date,
        category=category,
        country=getCountry(country),
        shop_name=shop_name
    )
    product.save()


categories_var = {
    'Випічка': [
        'bakery-varus', 'bakery', 'bakery-metro', 'bakery-ekomarket', 'bakery-auchan',
    ],
    'Фрукти та овочі': [
        'fruits-and-vegetables', 'fruits-and-vegetables-auchan', 'fruits-and-vegetables-varus', 'fruits-and-vegetables-ekomarket', 'fruits-and-vegetables-metro'
    ],
    'Снеки та солодощі': [
        'snacks-and-sweets', 'snacks-and-sweets-megamarket', 'snacks-and-sweets-varus', 'snacks-and-sweets-ekomarket', 'sweets-and-snacks-auchan', 'snacks-ekomarket', 'snacks-megamarket', 'snacks-and-sweets-metro'
    ],
    'Алкоголь': [
        'eighteen-plus', 'alcohol-varus', 'alcohol-megamarket', 'alcohol-ekomarket', 'eighteen-plus-auchan', 'eighteen-plus-metro'
    ],
    'Напої': [
        'drinks', 'drinks-varus', 'drinks-ekomarket', 'drinks-megamarket', 'drinks-auchan', 'hot-drinks-megamarket', 'hot-drinks-metro', 'hot-drinks-varus'
    ],
    'Консервація': ['canned-food-ekomarket', 'canned-food-oil-vinegar-metro', 'canned-food-auchan', 'canned-food-megamarket'],
    'Заморожені продукти': ['frozen', 'frozen-varus', 'frozen-auchan', 'frozen-megamarket', 'frozen-ekomarket', 'frozen-metro']
}


all_categories = [
    'bakery-varus', 'bakery', 'bakery-metro', 'bakery-ekomarket', 'bakery-auchan',
    'fruits-and-vegetables', 'fruits-and-vegetables-auchan', 'fruits-and-vegetables-varus', 'fruits-and-vegetables-ekomarket', 'fruits-and-vegetables-metro'
    'snacks-and-sweets', 'snacks-and-sweets-megamarket', 'snacks-and-sweets-varus', 'snacks-and-sweets-ekomarket', 'sweets-and-snacks-auchan', 'snacks-ekomarket', 'snacks-megamarket', 'snacks-and-sweets-metro',
    'eighteen-plus', 'alcohol-varus', 'alcohol-megamarket', 'alcohol-ekomarket', 'eighteen-plus-auchan', 'eighteen-plus-metro',
    'drinks', 'drinks-varus', 'drinks-ekomarket', 'drinks-megamarket', 'drinks-auchan', 'hot-drinks-megamarket', 'hot-drinks-metro', 'hot-drinks-varus',
    'canned-food-ekomarket', 'canned-food-oil-vinegar-metro', 'canned-food-auchan', 'canned-food-megamarket', 'frozen', 'frozen-varus', 'frozen-auchan', 'frozen-megamarket', 'frozen-ekomarket', 'frozen-metro'
]


def check_meaning(category):
    if category not in all_categories:
        return 'Інше'

    for cat, val in categories_var.items():
        if category in val:
            return cat


def split_json():
    get_file()
    with open('shop/static/json/data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    items = data['items']

    for item in items:
        if not item['storeQuantity']:
            continue

        if item['promoId'] == 'melkoopt':
            old_price = item['price']
            new_price = list(filter(lambda item: item['Type'] == 'specialPrice', item['prices']))[0]['Value']
            discount = item['promotions'][0]['description']
        else:
            new_price = item['price']
            old_price = item['oldPrice']
            discount = round((old_price - new_price) * (100.0 / old_price))

        country = list(filter(lambda item: item['key'] == 'country', item['parameters']))[0]['value']

        insert_into_table(
            item['name'], old_price, new_price, item['mainImage'], discount,
            item['promotion']['stopAfter'], 'alcohol', country, 'silpo'
        )


def parse_zakaz(url, name_of_shop, cat):
    page_count = 1
    while True:
        request = requests.get(url+str(page_count))
        print(url + str(page_count))
        page_count += 1
        if BeautifulSoup(request.text, 'html.parser').find("div", class_="ProductsBox") != None:    # check if link is actual
            try:
                soup = BeautifulSoup(request.text, 'html.parser')
                new_url = soup.find_all('a', class_="ProductTile", href=True)                       # find all products
                for i in new_url:
                    new_request = requests.get('https://'+name_of_shop+'.zakaz.ua/'+i['href'])
                    new_soup = BeautifulSoup(new_request.text, 'html.parser')

                    def get_country():
                        if new_soup.find('li', {'data-marker': 'Taxon country'}):                   # find country
                            return new_soup.find('li', {'data-marker': 'Taxon country'}).text.replace("Країна", "")
                        else:
                            return ''

                    insert_into_table(
                        new_soup.find('h1', class_="BigProductCardTopInfo__title").text,
                        i.find('span', class_='Price__value_minor').text,
                        i.find('span', class_='Price__value_discount').text,
                        i.find('img', {'loading': 'lazy'})['src'],
                        i.find('div', class_='ProductTile__badges').text,
                        i.find('span', class_='DiscountDisclaimer').text, cat, get_country(), name_of_shop)
            except Exception as ex:
                collect_errors(url, ex)
                print('Error')
        else:
            break


def parse_json(url, shop):
    response = requests.get(url, headers=headers)

    lib = response.json()
    buf = lib['results']
    for title in buf:
        insert_into_table(
            name=title['title'],
            slug=title['slug'] if title['slug'] in title else '',
            old_price=float(str(title['discount']['old_price'])[:-2]+'.'+str(title['discount']['old_price'])[-2:]),
            new_price=float(str(title['price'])[:-2] + '.' + str(title['price'])[-2:]),
            picture=title['img']["s150x150"],
            discount=title['discount']['value'],
            date=title['discount']['due_date'],
            category=check_meaning(title['parent_category_id']),
            country=title['country'],
            shop_name=shop
        )


@time_counter
def main_parse():
    urls = {
        'varus': 'https://stores-api.zakaz.ua/stores/48241001/products/promotion/?page=',
        'novus': 'https://stores-api.zakaz.ua/stores/48201070/products/promotion/?page=',
        'metro': 'https://stores-api.zakaz.ua/stores/48215611/products/promotion/?page=',
        'eko': 'https://stores-api.zakaz.ua/stores/48280214/products/promotion/?page=',
        'ashan': 'https://stores-api.zakaz.ua/stores/48246401/products/promotion/?page=',
        'mega': 'https://stores-api.zakaz.ua/stores/48267602/products/promotion/?page='
    }

    print('Parsing started')
    Product.objects.all().delete()  # clear table

    # Silpo
    # split_json()

    for i in urls.keys():
        count = 1
        while (requests.get(urls[i]+str(count), headers=headers).json())['results']:
            parse_json(urls[i]+str(count), i)
            count += 1

    print(
        len(Product.objects.all())
    )
