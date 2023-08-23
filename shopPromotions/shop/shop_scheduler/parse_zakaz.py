import requests
import json
import math

from .config import categories_zakaz, headers_zakaz
from shop.models import Product


all_categories: list = categories_zakaz.keys()

all_products_list: list = []


def insert_new_products(shop_name: str, products: json):
    errors_number = 0
    for product in products:
        discount = product.get('discount')
        old_price = int(discount.get('old_price'))/100
        new_price = int(product.get('price'))/100

        name = product.get('title')
        slug = product.get('slug')

        category = product.get('parent_category_id')
        country = product.get('country')

        if not old_price or not new_price:
            errors_number += 1
            continue

        new_product = Product(
            name=name,
            slug_nam=slug,
            old_price=old_price,
            new_price=new_price,
            picture=product.get('img').get('s150x150'),
            percent_of_sale=int((old_price-new_price)/old_price*100),
            date_of_end=discount.get('due_date'),
            category=categories_zakaz.get(category),
            country=country,
            shop_name=shop_name
        )

        all_products_list.append(new_product)


def parse_specific_shop(shop_name: str, shop_url: str):
    current_page_number = 0
    response = requests.get(f'{shop_url}{1}', headers=headers_zakaz).json()

    # Number of pages variable is needed to know how many pages need to be requested
    number_of_pages = math.ceil(int(response['count'])/30)

    while current_page_number != number_of_pages:
        current_page_number += 1
        page_url = f'{shop_url}{current_page_number}'

        response = requests.get(
            url=page_url, 
            headers=headers_zakaz
        ).json()
    
        insert_new_products(shop_name, response.get('results'))


def parse_zakaz():
    store_codes = {
        'varus': '48241001',
        'novus': '48201070',
        'metro': '48215611',
        'eko': '48280214',
        'ashan': '48246401',
        'mega': '48267602'
    }

    for store_name, store_code in store_codes.items():
        print(store_name)
        base_url = f'https://stores-api.zakaz.ua/stores/{store_code}/products/promotion/?page='
        parse_specific_shop(store_name, base_url)

    # Insert new products from zakaz.ua into DB using bulk insertion
    Product.objects.bulk_create(all_products_list)

    # Clear list of products
    all_products_list.clear()

    print(f'Number of products = {len(all_products_list)}')