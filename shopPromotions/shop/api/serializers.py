from rest_framework import serializers

from shop.models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'name', 'slug_nam', 'old_price', 'new_price', 
            'percent_of_sale', 'date_of_end', 'category', 
            'country', 'shop_name'
        ]
