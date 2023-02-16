import json

import jsonfield as jsonfield
from django.db import models
from datetime import date

from django.urls import reverse


# class User(models.Model):
#     username = models.CharField(max_length=255, verbose_name="Имя пользователя")
#     password = models.CharField(max_length=20, verbose_name="Пароль")
#     mail = models.CharField(max_length=30, verbose_name="Почта")
#     date_of_registration = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
#
#     class Meta:
#         verbose_name_plural = "Користувачі"
#         ordering = ['username', 'mail']


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    slug_nam = models.SlugField(max_length=255)
    old_price = models.FloatField(max_length=20, verbose_name="Старая цена")
    new_price = models.FloatField(max_length=20, verbose_name="Новая цена")
    # picture = models.ImageField(upload_to='images/', verbose_name="Фото")
    picture = models.CharField(max_length=100, verbose_name="Фото")
    percent_of_sale = models.IntegerField(verbose_name="Скидка")
    date_of_end = models.CharField(max_length=10, verbose_name="Окончание")
    category = models.CharField(max_length=20, verbose_name="Категория")
    country = models.CharField(max_length=20, default=None, verbose_name="Страна")
    shop_name = models.CharField(max_length=20, verbose_name="Магазин")
    # shop_name = models.ForeignKey("Shop", on_delete=models.PROTECT, null=True, verbose_name="Магазин")

    class Meta:
        verbose_name = "Продукты"
        verbose_name_plural = "Продукты"
        ordering = ['name', 'category']

    def image_tag(self):
        from django.utils.html import mark_safe
        return mark_safe(f'<img src="{self.picture}" width="100" />')
        # return mark_safe('<img src="{}" width="100" />'.format(self.picture.url))
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    # def absolute_url(self):
    #     return reverse('name', kwargs={'shop': self.name})


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


# class Shop(models.Model):
#     name = models.CharField(max_length=100, verbose_name="Название")
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = "Магазины"
#         verbose_name_plural = "Магазины"
#         # ordering = ['name']
