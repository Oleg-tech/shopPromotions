from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *


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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
