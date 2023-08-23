import requests
import json

from shop.models import Product
from .config import headers_silpo, get_data_for_silpo_request, data_count


silpo_categories = {
    22: 'Алкоголь',
    52: 'Напої',
    65: 'Бакалія',
    130: 'Консервація, соуси та спеції',
    234: 'Молочне, яйця, сир',
    264: 'Заморожені продукти',
    277: 'M\'ясо, риба, птиця',
    308: 'Снеки та солодощі',
    316: 'M\'ясо, риба, птиця',
    359: 'Напої',
    374: 'Фрукти та овочі',
    433: 'Випічка',
    449: 'Дитячі товари',
    476: 'Квіти, товари для саду та городу',
    486: 'Хліб та хлібобулочні вироби',
    498: 'Снеки та солодощі',
    535: 'Гігієна',
    567: 'Для дому',
    653: 'Для тварин',
    1468: 'Молочне, яйця, сир',
    4384: '18+',
    None: 'Інше',
}

all_products_list: list = []


def insert_new_products(shop_name: str, products: json):
    errors_number = 0
    for product in products:
        old_price = product.get('prices')[0].get('Value')
        new_price = product.get('prices')[1].get('Value')
        name = product.get('name')
        slug = product.get('slug')

        category = product.get('categories')
        if category:
            category = category[0].get('id')

        parameters = product.get('parameters')
        country = None
        if parameters:
            for param in parameters:
                if param.get('key') == 'country':
                    country = param.get('value')
                    break

        if not old_price or not new_price:
            errors_number += 1
            continue

        new_product = Product(
            name=name,
            slug_nam=slug,
            old_price=old_price,
            new_price=new_price,
            picture=product.get('mainImage'),
            percent_of_sale=int((old_price-new_price)/old_price*100),
            date_of_end=product.get('priceStopAfter'),
            category=silpo_categories.get(category),
            country=country,
            shop_name=shop_name,
        )

        all_products_list.append(new_product)

    print(f'Number of errors = {errors_number}')
    print(f'Number of products = {len(all_products_list)}')


def parse_silpo():
    url = 'https://api.catalog.ecom.silpo.ua/api/2.0/exec/EcomCatalogGlobal'

    # Calculate number of products with sale in Silpo
    response = requests.post(url=url, data=data_count, headers=headers_silpo).json()
    sale_categories = response['filters'][0]['props']['items']

    products_amount = 0
    for category in sale_categories:
        products_amount += category['itemsCount']

    # Get all products with sales from Silpo
    data = get_data_for_silpo_request(product_amount=products_amount)
    response = requests.post(url=url, data=data, headers=headers_silpo).json()
    products = response['items'] 

    insert_new_products(shop_name='silpo', products=products)

    # Insert new products from Silpo into DB using bulk insertion
    Product.objects.bulk_create(all_products_list)

    # Clear list of products
    all_products_list.clear()
