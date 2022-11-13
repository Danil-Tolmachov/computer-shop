from django.contrib.auth import login
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator as token_generator

from cart.models import Cart
from register.models import ShopUser
from register.utils import get_uid, get_verify_token


class UserCreationTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        email = 'testmail@testmail.com'
        password = 'testpass'
        ShopUser.objects.create_user(email=email,
                                     password=password,
                                     first_name='TestFirstName',
                                     last_name='TestLastName',
                                     country='Ukraine',
                                     city='Kyiv',
                                     address='Kryshatik, 132',
                                     )

    def test_create_user(self):
        user = ShopUser.objects.first()

        self.assertFalse(user.is_active)
        self.assertTrue(user.first_name)
        self.assertTrue(user.last_name)
        self.assertTrue(user.country)
        self.assertTrue(user.city)
        self.assertTrue(user.address)

    def test_user_cart(self):
        user = ShopUser.objects.first()

        self.assertEqual(user.cart, Cart.objects.first())

    @classmethod
    def tearDownClass(cls):
        user = ShopUser.objects.first()
        user.delete()


class UserVerificationTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        email = 'testmail@testmail.com'
        password = 'testpass'
        ShopUser.objects.create_user(email=email, password=password)

    def test_uid(self):
        user = ShopUser.objects.first()
        user_pk = str(user.pk)
        decoded_uid = force_str(urlsafe_base64_decode(get_uid(user)))

        self.assertEqual(user_pk, decoded_uid)

    def test_tokens(self):
        user = ShopUser.objects.first()
        token = get_verify_token(user)

        self.assertTrue(token_generator.check_token(user, token))

    def test_verify_url(self):
        user = ShopUser.objects.first()
        uid = get_uid(user)
        token = get_verify_token(user)

        self.assertFalse(user.is_active)

        response = self.client.get(reverse('activate', args=[uid, token]))
        user = response.wsgi_request.user

        self.assertTrue(user.is_active)
