from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from shop.views import (
    create_user, AdminLoginView, user_exit, main_page,
    products, selected, ShowProduct, filter_data, load_more_data, 
    delete_selected_from_model, add_selected_to_model
)
from shop.api.api_views import ProductViewSet


router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')


urlpatterns = [
    #   user profile control
    path('registration/', create_user, name='register'),
    path('login/', AdminLoginView.as_view(), name='login'),
    path('logout/', user_exit, name='logout'),

    #   shop functions
    path('', main_page, name='home'),
    path('products/', products, name='products'),
    path('selected', selected, name='selected'),
    path('products/<slug:product_id>', ShowProduct.as_view(), name='showproduct'),

    #   ajax
    path('filter-data', filter_data, name='filter_data'),
    path('load-more-data', load_more_data, name='load_more_data'),
    path('delete_selected_from_model', delete_selected_from_model, name='delete_selected_from_model'),
    path('add_selected_to_model', add_selected_to_model, name='add_selected_to_model'),

    # API
    path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
