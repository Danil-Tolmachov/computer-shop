import json
from django.utils.http import urlsafe_base64_encode
from django.contrib import admin
from django.db import models
from django.db.models import ManyToManyField, CharField, ForeignKey, \
    BooleanField, IntegerField, JSONField, \
    ImageField, TextField, DateTimeField, QuerySet
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.core.exceptions import ValidationError

from auth_app.utils import get_users_by_ids


class Order(models.Model):
    SUBMITTED = 'SUBMITTED'
    PROCEED = 'PROCEED'
    ISSUED_TO_THE_CARRIER = 'ISSUED TO THE CARRIER'
    SHIPPED = 'Shipped'
    FINISHED = 'Finished'
    CANCELED = 'Canceled'


    STATUS_CHOICE = (
        (SUBMITTED, 'Submitted'),
        (PROCEED, 'Processed'),
        (ISSUED_TO_THE_CARRIER, 'Issued to the carrier'),
        (SHIPPED, 'Shipped'),
        (FINISHED, 'Finished'),
        (CANCELED, 'Canceled'),
    )


    url = CharField(max_length=255)

    status = CharField(max_length=255, choices=STATUS_CHOICE, default=SUBMITTED)
    status_comment = CharField(max_length=255, default='', blank=True)

    products = ManyToManyField('ProductItem', related_name='order')

    date_created = DateTimeField(default=timezone.now)

    is_paid = BooleanField(default=False)
    is_closed = BooleanField(default=False)


    def __str__(self):
        return str(self.pk)


    def encoded(self):
        """
            Returns order url id
        """
        return urlsafe_base64_encode(force_bytes(self.pk))


    def get_sum(self):
        """
            Returns summary price of all products in order
        """
        return sum(map(lambda x: x.get_summary(), self.products.all()))


    @admin.display(description='Products count')
    def get_products_count(self) -> int:
        return self.products.count()


    @admin.display(description='Customer')
    def get_customer_name(self) -> str:
        """
            Shows user email in admin paner
        """

        if self.shopuser.first():
            return self.shopuser.first().email
        else:
            return 'Deleted User'


    @admin.display(description='Summary')
    def get_summary(self) -> int:
        """
            Shows summary price in admin panel
        """

        return self.get_sum()



class Category(models.Model):
    
    category_name = CharField(max_length=45)
    category_slug = CharField(max_length=80, null=True, blank=True)


    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


    def __str__(self):
        return self.category_name


    @admin.display(description='Products')
    def get_product_count(self) -> int:
        return self.product_set.count()



class ProductImage(models.Model):

    image = ImageField(upload_to='product_images')

    def __str__(self):

        product = self.product_set.first()

        if product:
            return product.name

        else:
            return f"({self.pk}){self.image}"



class Product(models.Model):

    name = CharField(max_length=255, blank=True)
    images = ManyToManyField('ProductImage', blank=True)

    text = TextField(null=True, blank=True)

    category = ForeignKey('Category', on_delete=models.SET_DEFAULT, default=1)

    price = IntegerField()
    available_count = ManyToManyField('Storage', blank=True)
    characteristics = JSONField(null=True, blank=True)

    comments = JSONField(null=True, blank=True, default=dict)

    is_visible = BooleanField(default=True)
    is_available = BooleanField(default=False)


    def __str__(self):
        return self.name


    def get_storage_objects(self) -> QuerySet:
        return self.product_item.filter(storage__isnull=False)


    def validate_product_comment(self, comment):
        """
            Validates comment
        """

        try:
            comment['author']
            comment['content']
            comment['is_positive']
        except KeyError:
            raise ValidationError


    def save_product_comment(self, new_comment):
        """
            Saves comment to db
        """

        try:
            comments = json.loads(str(self.comments))     
        except json.JSONDecodeError:
            comments = []

        comments.append(new_comment)

        self.comments = json.dumps(comments)
        self.save()


    def add_comment(self, author, content, is_positive):

        new_comment = {
            'author': author.pk,
            'content': content,
            'is_positive': is_positive,
        }

        self.validate_product_comment(new_comment)
        self.save_product_comment(new_comment)


    @staticmethod
    def load_comments_authors(comments):

        authors = []

        # Get author ids
        for comment in comments:
            authors.append(comment['author'])
        
        # Get authors query
        authors_query = get_users_by_ids(authors)

        # Replace author ids by objects
        for comment, author in zip(comments, authors_query):
            comment['author'] = author

        return comments


    def get_comments(self):

        # Load comments to list
        comments = json.loads(str(self.comments))

        # Load authors to list
        comments = self.load_comments_authors(comments)

        return comments


    @admin.display(description='Count')
    def get_all_count(self) -> int:
        """
            Shows count of ordered and storaged product
        """
        
        storages_count = sum(map(lambda x: x.product_count,
                                 self.product_item.filter(storage__isnull=False)
                                 ))

        orders_count = sum(map(lambda x: x.product_count,
                               self.product_item.filter(order__isnull=False)
                               ))

        return storages_count + orders_count



class ProductItem(models.Model):

    product = ForeignKey('Product', on_delete=models.CASCADE, related_name='product_item')
    product_count = IntegerField()


    def __str__(self):
        return f"{self.product} / {self.product_count} / {self.get_source()}"


    def get_summary(self) -> int:
        return self.product.price * self.product_count


    @admin.display(description='Source')
    def get_source(self) -> str:
        return 'Order' if self.order.first() else 'Storage' if self.storage.first() else 'Cart'


    @admin.display(description='Related source')
    def get_related_id(self) -> str:
        return self.order.first() or self.user.first()



class Storage(models.Model):

    country = CharField(max_length=70)
    city = CharField(max_length=70)
    address = CharField(max_length=255)

    products = ManyToManyField('ProductItem', related_name='storage', blank=True)


    @admin.display(description='Positions count')
    def get_positions_count(self) -> int:
        return self.products.count() if self.products else 0

    def __str__(self):
        return f"{self.country}, {self.city}"
