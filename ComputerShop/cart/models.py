from django.contrib import admin
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models import ManyToManyField, CharField, ForeignKey, BooleanField, IntegerField, JSONField, ImageField, \
    URLField, TextField

from ComputerShop.settings import MEDIA_URL


class Cart(models.Model):
    products = ManyToManyField('Product')


class Order(models.Model):

    STATUS_CHOICE = (
        ('submitted', 'Submitted'),
        ('processed', 'Processed'),
        ('issued to the carrier', 'Issued to the carrier'),
        ('shipped', 'Shipped'),
        ('Finished', 'Finished'),
    )

    status = CharField(max_length=255, choices=STATUS_CHOICE, default=STATUS_CHOICE[0])
    status_comment = CharField(max_length=255, blank=True)

    products = ManyToManyField('Product')

    is_paid = BooleanField(default=False)
    is_closed = BooleanField(default=False)

    @admin.display(description='Products count')
    def get_products_count(self):
        return self.products.count()

    @admin.display(description='Customer')
    def get_customer_name(self):
        if self.shopuser.first():
            return self.shopuser.first().email
        else:
            return 'Deleted User'

    @admin.display(description='Summary')
    def get_sum(self):
        return sum(map(lambda x: x.price, self.products.all()))


class Category(models.Model):
    category_name = CharField(max_length=45)
    category_slug = CharField(max_length=80, null=True, blank=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


#class ImageManager(models.Manager):
#
#    def create(self, image):
#        fss = FileSystemStorage(location='media/product_images/')
#        file_id = ProductImage.objects.count()+1
#        file = fss.save(name=file_id, content=image)
#        url = MEDIA_URL + f'product_images/{file}'
#
#        obj = self.model(url=url)
#        self._for_write = True
#
#        obj.save(force_insert=True, using=self.db)
#        return obj


class ProductImage(models.Model):
    image = ImageField(upload_to='product_images')


class Product(models.Model):
    name = CharField(max_length=255)
    images = ManyToManyField('ProductImage', null=True, blank=True)

    text = TextField(null=True, blank=True)

    category = ForeignKey('Category', on_delete=models.SET_DEFAULT, default=1)

    price = IntegerField()
    available_count = ManyToManyField('Storage', blank=True)
    characteristics = JSONField(null=True, blank=True)

    is_visible = BooleanField(default=True)
    is_available = BooleanField(default=False)

    def __str__(self):
        return self.name


class Storage(models.Model):
    country = CharField(max_length=70)
    city = CharField(max_length=70)
    address = CharField(max_length=255)

    products = ManyToManyField('Product', blank=True)

    @admin.display(description='Positions count')
    def get_positions_count(self):
        if self.products:
            return self.products.count()
        else:
            return 0

    def __str__(self):
        return f"{self.country}, {self.city}"
