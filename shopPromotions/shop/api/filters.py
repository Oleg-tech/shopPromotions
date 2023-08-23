from django_filters import rest_framework as filters

from shop.models import Product


class ProductsFilter(filters.FilterSet):
    shop = filters.CharFilter(field_name='shop_name', lookup_expr='contains')
    category = filters.CharFilter(field_name='category', lookup_expr='exact')
    country = filters.CharFilter(field_name='country', lookup_expr='exact')

    class Meta:
        model = Product
        fields = ['shop', 'category','country']
