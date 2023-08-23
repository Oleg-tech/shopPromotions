import time

def time_counter(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        elapsed_time = end_time - start_time
        print(f"Time = {elapsed_time}")
        return result
    return wrapper

# Configurations for zakaz.ua
headers_zakaz = {
    'Content-type': 'application/json',
    'Accept': 'application/json',
    'Accept-Language': 'uk'
}


def get_data_for_zakaz_request(product_amount):
    data = f"""
    {{
        "method": "GetSimpleCatalogItems",
        "data":
        {{
            "CategoryFilter": [],
            "From": 1,
            "MultiFilters": "",
            "Promos": [],
            "RangeFilters": "",
            "To": {product_amount},
            "UniversalFilters": [],
            "basketGuid": "",
            "businessId": 1,
            "deliveryType": 2,
            "filialId": 3288,
            "ingredients": "false",
            "merchantId": 1,
            "onlyPromo": "true",
        }}
    }}
    """

    return data


categories_zakaz: dict = {
    'bakery-varus': 'Випічка',
    'bakery': 'Випічка',
    'bakery-metro': 'Випічка',
    'bakery-ekomarket': 'Випічка',
    'bakery-auchan': 'Випічка',

    'fruits-and-vegetables': 'Фрукти та овочі',
    'fruits-and-vegetables-auchan': 'Фрукти та овочі',
    'fruits-and-vegetables-varus': 'Фрукти та овочі',
    'fruits-and-vegetables-ekomarket': 'Фрукти та овочі',
    'fruits-and-vegetables-metro': 'Фрукти та овочі',

    'snacks-and-sweets': 'Снеки та солодощі',
    'snacks-and-sweets-megamarket': 'Снеки та солодощі',
    'snacks-and-sweets-varus': 'Снеки та солодощі',
    'snacks-and-sweets-ekomarket': 'Снеки та солодощі',
    'sweets-and-snacks-auchan': 'Снеки та солодощі',
    'snacks-ekomarket': 'Снеки та солодощі',
    'snacks-megamarket': 'Снеки та солодощі',
    'snacks-and-sweets-metro': 'Снеки та солодощі',
    'snacks-varus': 'Снеки та солодощі',
    'packets-cereals': 'Снеки та солодощі',
    'crisps-and-snacks': 'Снеки та солодощі',
    'crisps-and-snacks-metro': 'Снеки та солодощі',
    'packets-cereals-metro': 'Снеки та солодощі',
    'crisps-and-snacks-auchan': 'Снеки та солодощі',

    'eighteen-plus': 'Алкоголь',
    'alcohol-varus': 'Алкоголь',
    'alcohol-megamarket': 'Алкоголь',
    'alcohol-ekomarket': 'Алкоголь',
    'eighteen-plus-auchan': 'Алкоголь',
    'eighteen-plus-metro': 'Алкоголь',

    'drinks': 'Напої',
    'drinks-varus': 'Напої',
    'drinks-ekomarket': 'Напої',
    'drinks-megamarket': 'Напої',
    'drinks-auchan': 'Напої',
    'drinks-metro': 'Напої',
    'hot-drinks-megamarket': 'Напої',
    'hot-drinks-metro': 'Напої',
    'hot-drinks-varus': 'Напої',
    'hot-drinks-novus': 'Напої',
    'hot-drinks-ekomarket': 'Напої',
    'hot-drinks-auchan': 'Напої',

    'canned-food-ekomarket': 'Консервація, соуси та спеції',
    'canned-food-oil-vinegar-metro': 'Консервація, соуси та спеції',
    'canned-food-auchan': 'Консервація, соуси та спеції',
    'canned-food-megamarket': 'Консервація, соуси та спеції',
    'canned-food-varus': 'Консервація, соуси та спеції',

    'frozen': 'Заморожені продукти',
    'frozen-varus': 'Заморожені продукти',
    'frozen-auchan': 'Заморожені продукти',
    'frozen-megamarket': 'Заморожені продукти',
    'frozen-ekomarket': 'Заморожені продукти',
    'frozen-metro': 'Заморожені продукти',

    'dairy-and-eggs-varus': 'Молочне, яйця, сир',
    'dairy-and-eggs': 'Молочне, яйця, сир',
    'dairy-and-eggs-metro': 'Молочне, яйця, сир',
    'dairy-and-eggs-ekomarket': 'Молочне, яйця, сир',
    'dairy-and-eggs-auchan': 'Молочне, яйця, сир',
    'dairy-and-eggs-megamarket': 'Молочне, яйця, сир',

    'meat-fish-poultry-varus': 'М\'ясо, риба, птиця',
    'meat-fish-poultry': 'М\'ясо, риба, птиця',
    'meat-fish-poultry-metro': 'М\'ясо, риба, птиця',
    'meat-fish-poultry-ekomarket': 'М\'ясо, риба, птиця',
    'meat-fish-poultry-auchan': 'М\'ясо, риба, птиця',
    'meat-fish-poultry-megamarket': 'М\'ясо, риба, птиця',

    'grocery-varus': 'Бакалія',
    'grocery-ekomarket': 'Бакалія',
    'grocery-and-sweets-auchan': 'Бакалія',
    'grocery-megamarket': 'Бакалія',

    'sauces-and-spices-varus': 'Консервація, соуси та спеції',
    'sauces-and-spices-novus': 'Консервація, соуси та спеції',
    'sauces-and-spices-metro': 'Консервація, соуси та спеції',
    'sauces-and-spices-ekomarket': 'Консервація, соуси та спеції',
    'sauces-and-spices-auchan': 'Консервація, соуси та спеції',
    'sauces-and-spices-megamarket': 'Консервація, соуси та спеції',

    'ready-meals-varus': 'Готові страви',
    'ready-meals': 'Готові страви',
    'ready-meals-auchan': 'Готові страви',

    'for-animals-varus': 'Для тварин',
    'for-animals': 'Для тварин',
    'for-animals-metro': 'Для тварин',
    'for-animals-ekomarket': 'Для тварин',
    'for-animals-auchan': 'Для тварин',

    'household-chemicals': 'Для дому',
    'household-goods-varus': 'Для дому',
    'household-chemicals-auchan': 'Для дому',
    'household-and-pets-care-auchan': 'Для дому',
    'household-goods-metro': 'Для дому',
    'household-goods-megamarket': 'Для дому',
    'household-and-cleaning': 'Для дому',
    'household-goods-ekomarket': 'Для дому',

    'kitchenware': 'Для дому',
    'kitchenware-varus': 'Для дому',
    'kitchenware-auchan': 'Для дому',
    'kitchenware-megamarket': 'Для дому',
    'kitchenware-metro': 'Для дому',
    'kitchenware-ekomarket': 'Для дому',

    'interior-and-textiles-varus': 'Для дому',
    'home-interior-and-textiles-metro': 'Для дому',

    'hygiene': 'Гігієна',
    'hygiene-auchan': 'Гігієна',
    'personal-hygiene': 'Гігієна',
    'personal-hygiene-varus': 'Гігієна',
    'personal-hygiene-metro': 'Гігієна',
    'personal-care-cosmetics-perfumes-metro': 'Гігієна',
    'personal-hygiene-ekomarket': 'Гігієна',
    'personal-hygiene-auchan': 'Гігієна',
    'personal-hygiene-megamarket': 'Гігієна',

    'chemicals-varus': 'Інше',
    'cosmetics-and-care-varus': 'Інше',
    'babies-varus': 'Інше',
    'all-stationery-varus': 'Інше',
    'clothes-and-shoes-varus': 'Інше',
    'hobby-and-rest-varus': 'Інше',
    'tins-jars-cooking': 'Інше',
    'babies': 'Інше',
    'stationery': 'Інше',
    'hobby': 'Інше',
    'clothes-and-shoes-novus': 'Інше',
    'tobacco-goods': 'Інше',
    'chemicals-metro': 'Інше',
    'babies-metro': 'Інше',
    'stationery-metro': 'Інше',
    'hobby-and-rest-metro': 'Інше',
    'chemicals-ekomarket': 'Інше',
    'hobby-and-rest-ekomarket': 'Інше',
    'all-stationery-ekomarket': 'Інше',
    'clothes-and-shoes-ekomarket': 'Інше',
    'babies-ekomarket': 'Інше',
    'interior-and-textiles-ekomarket': 'Інше',
    'cosmetics-and-care-ekomarket': 'Інше',
    'bioproducts-and-diabetic-goods-auchan': 'Інше',
    'stationery-auchan': 'Інше',
    'babies-auchan': 'Інше',
    'gourmet-auchan': 'Інше',
    'hobby-auchan': 'Інше',
    'clothes-auchan': 'Інше',
    'chemicals-megamarket': 'Інше',
    'babies-megamarket': 'Інше',
    'cosmetics-and-care-megamarket': 'Інше',

    None: 'Інше'
}

# Configurations for Silpo
headers_silpo = {
    'Content-type': 'application/json',
    'Accept': 'application/json'
}

def get_data_for_silpo_request(product_amount):
    data = f"""
    {{
        "method": "GetSimpleCatalogItems",
        "data":
        {{
            "CategoryFilter": [],
            "From": 1,
            "MultiFilters": "",
            "Promos": [],
            "RangeFilters": "",
            "To": {product_amount},
            "UniversalFilters": [],
            "basketGuid": "",
            "businessId": 1,
            "deliveryType": 2,
            "filialId": 3288,
            "ingredients": "false",
            "merchantId": 1,
            "onlyPromo": "true",
        }}
    }}
    """

    return data


data_count = """
{
    method: "GetPromoFilters",
    "data":
    {
        merchantId: 1, 
        basketGuid: "", 
        deliveryType: 2, 
        promoId: null, 
        filialId: 3288, 
        setId: null
    }
}
"""
