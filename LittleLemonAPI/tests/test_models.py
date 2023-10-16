from ..models import *
from django.contrib.auth.models import User
from django.test import TestCase, Client



class OrderTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.data = {"username":"test", "password":"testUser12345!"}
        cls.user = User.objects.create_user(**cls.data)
        cls.category = Category.objects.create(slug="protein", title="Protein")
        cls.menuitem = MenuItem.objects.create(
            title="Chicken", 
            price = 2.30,
            featured=False,
            category=cls.category)
        cls.cart = Cart.objects.create(
            user=cls.user
        )
