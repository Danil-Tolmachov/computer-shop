from django.test import TestCase

from cart.models import Product
from register.models import ShopUser


class OrderTest(TestCase):

    UserForm = {
        'email': 'testmail@testmail.com',
        'password': 'testpass',
        'first_name': 'TestFirstName',
        'last_name': 'TestLastName',
        'country': 'Ukraine',
        'city': 'Kyiv',
        'address': 'Kryshatik, 132',
    }

    @classmethod
    def setUpTestData(cls):
        # Users
        ShopUser.objects.create_user(**cls.UserForm)

        OrderTest.UserForm.update(email='testmail2@testmail.com')
        ShopUser.objects.create_user(**cls.UserForm)

        OrderTest.UserForm.update(email='testmail3@testmail.com')
        ShopUser.objects.create_user(**cls.UserForm)

        OrderTest.UserForm.update(email='testmail4@testmail.com')
        ShopUser.objects.create_user(**cls.UserForm)

        OrderTest.UserForm.update(email='testmail5@testmail.com')
        ShopUser.objects.create_user(**cls.UserForm)

        # Products

        Product.objects.create(name='GTX 1060', price=200, is_available=True)
        Product.objects.create(name='GTX 1080', price=300)

    def test_users_and_carts_addition_after_delete(self):
        ShopUser.objects.get(pk=2).delete()
        ShopUser.objects.get(pk=4).delete()

        OrderTest.UserForm.update(email='testmail4@testmail.com')
        self.user4 = ShopUser.objects.create_user(**OrderTest.UserForm)

        OrderTest.UserForm.update(email='testmail2@testmail.com')
        self.user2 = ShopUser.objects.create_user(**OrderTest.UserForm)

        self.assertEqual(5, ShopUser.objects.count())

    def test_order_creation(self):

        user2 = ShopUser.objects.get(pk=2)
        prod = Product.objects.get(pk=1)

        user2.cart.add(prod)
