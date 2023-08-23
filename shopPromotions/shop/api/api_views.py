from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter

from shop.models import Product
from .serializers import ProductSerializer
from .filters import ProductsFilter


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    filter_backends = (
        DjangoFilterBackend, OrderingFilter, SearchFilter,
    )
    filterset_class = ProductsFilter
    ordering_fields = ('percent_of_sale', )
    search_fields = ('name', 'country', )
