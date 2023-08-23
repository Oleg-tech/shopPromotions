from django.contrib import admin

from .models import Product, SelectedProductsAnonymous, Mailing


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'slug_nam', 'old_price', 'new_price', 'percent_of_sale',
        'date_of_end', 'image_tag'
    ]
    list_display_links = ['name']
    list_filter = ['category', 'shop_name']    # filters for products
    search_fields = ['category', ]
    prepopulated_fields = {'slug_nam': ['name',]}


class SelectedAdmin(admin.ModelAdmin):
    list_display = [
        'user_ip', 'product_id'
    ]
    list_display_links = ['user_ip']


class MailingAdmin(admin.ModelAdmin):
    list_display = [
        'user_id'
    ]


admin.site.register(Product, ProductAdmin)  # adds Products to admin panel
admin.site.register(SelectedProductsAnonymous, SelectedAdmin)
admin.site.register(Mailing, MailingAdmin)
