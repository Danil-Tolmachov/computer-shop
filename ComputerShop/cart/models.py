from django.db import models
from django.db.models import ManyToManyField, CharField, ForeignKey, BooleanField, IntegerField, JSONField



class Cart(models.Model):
    products = ManyToManyField('Product')


class Order(models.Model):
    status = CharField(max_length=255)

    products = ManyToManyField('Product')

    is_paid = BooleanField(default=False)


class Category(models.Model):
    category_name = CharField(max_length=255)
    category_slug = CharField(max_length=255)


class Product(models.Model):
    name = CharField(max_length=255)
    category = ForeignKey('Category', on_delete=models.CASCADE, null=True)

    price = IntegerField()
    available_count = ManyToManyField('Storage')
    characteristics = JSONField(null=True)

    is_visible = BooleanField(default=True)
    is_available = BooleanField(default=False)


class Storage(models.Model):
    country = CharField(max_length=70)
    city = CharField(max_length=70)
    address = CharField(max_length=255)

    products = ForeignKey('Product', on_delete=models.CASCADE)

