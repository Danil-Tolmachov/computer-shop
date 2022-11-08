from django.contrib import admin
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models import ManyToManyField, CharField, ForeignKey, BooleanField, IntegerField, JSONField, ImageField, \
    URLField, TextField, DateTimeField
from django.utils import timezone


class Cart(models.Model):
    products = ManyToManyField('ProductItem')

    def get_order(self, request, order_url):
        self.order = Order.objects.create(url=order_url)
        self.order.products.add(*request.user.cart.products.all())
        return self.order


class Order(models.Model):
    SUBMITTED = 'SUBMITTED'
    PROCEED = 'PROCEED'
    ISSUED_TO_THE_CARRIER = 'ISSUED TO THE CARRIER'
    SHIPPED = 'Shipped'
    FINISHED = 'Finished'

    STATUS_CHOICE = (
        (SUBMITTED, 'Submitted'),
        (PROCEED, 'Processed'),
        (ISSUED_TO_THE_CARRIER, 'Issued to the carrier'),
        (SHIPPED, 'Shipped'),
        (FINISHED, 'Finished'),
    )

    url = CharField(max_length=255)

    status = CharField(max_length=255, choices=STATUS_CHOICE, default=SUBMITTED)
    status_comment = CharField(max_length=255, default='', blank=True)

    products = ManyToManyField('ProductItem')

    date_created = DateTimeField(default=timezone.now)

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

    # Get cart items summary price
    @admin.display(description='Summary')
    def get_summary(self):
        return sum(map(lambda x: x.get_summary(), self.products.all()))


class Category(models.Model):
    category_name = CharField(max_length=45)
    category_slug = CharField(max_length=80, null=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name

    @admin.display(description='Products')
    def get_product_count(self):
        return self.product_set.count()


class ProductImage(models.Model):
    image = ImageField(upload_to='product_images')

    def __str__(self):
        if self.product_set.first():
            return self.product_set.first().name
        else:
            return f"({self.pk}){self.image}"


class Product(models.Model):
    name = CharField(max_length=255)
    images = ManyToManyField('ProductImage', blank=True)

    text = TextField(null=True, blank=True)

    category = ForeignKey('Category', on_delete=models.SET_DEFAULT, default=1)

    price = IntegerField()
    available_count = ManyToManyField('Storage', blank=True)
    characteristics = JSONField(null=True, blank=True)

    is_visible = BooleanField(default=True)
    is_available = BooleanField(default=False)

    def __str__(self):
        return self.name


class ProductItem(models.Model):
    product = ForeignKey('Product', on_delete=models.CASCADE)
    product_count = IntegerField()

    def get_summary(self):
        return self.product.price * self.product_count


class Storage(models.Model):
    country = CharField(max_length=70)
    city = CharField(max_length=70)
    address = CharField(max_length=255)

    products = ManyToManyField('ProductItem', blank=True)

    @admin.display(description='Positions count')
    def get_positions_count(self):
        return self.products.count() if self.products else 0

    def __str__(self):
        return f"{self.country}, {self.city}"
