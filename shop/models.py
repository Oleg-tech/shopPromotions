import jsonfield as jsonfield
from django.db import models

from django.utils.html import mark_safe


class Product(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="Назва"
    )
    slug_nam = models.SlugField(
        max_length=255
    )
    old_price = models.FloatField(
        max_length=20, verbose_name="Стара ціна"
    )
    new_price = models.FloatField(
        max_length=20, verbose_name="Нова ціна"
    )
    picture = models.CharField(
        max_length=100, default=None, null=True, verbose_name="Фото"
    )
    percent_of_sale = models.IntegerField(
        verbose_name="Знижка"
    )
    date_of_end = models.CharField(
        max_length=10, verbose_name="Діє до"
    )
    category = models.CharField(
        max_length=50, verbose_name="Категорія"
    )
    country = models.CharField(
        max_length=20, default=None, null=True, verbose_name="Країна походження"
    )
    shop_name = models.CharField(
        max_length=20, verbose_name="Магазин"
    )

    class Meta:
        verbose_name = "Продукти"
        verbose_name_plural = "Продукти"
        ordering = ['name', 'category']

    def image_tag(self):
        return mark_safe(f'<img src="{self.picture}" width="100" />')

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


class SelectedProductsAnonymous(models.Model):
    user_ip = models.CharField(max_length=30, verbose_name="IP")
    product_id = models.IntegerField()


class Mailing(models.Model):
    user_id = models.EmailField()
    mailing_objects = jsonfield.JSONField(default=None)

    def get_value(self):
        print('True', self)
        print(self.__dict__)
        print(self.x)
        # return self.shops
