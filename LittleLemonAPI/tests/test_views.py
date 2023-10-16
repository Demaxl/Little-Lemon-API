from ..models import *
from django.contrib.auth.models import User, Group
from django.test import Client, TestCase

import json



class UserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.data = {"username":"test", "password":"testUser12345!"}
        cls.user = User.objects.create_user(**cls.data)
        cls.client = Client()

        token = "651847910c348d9071ff2f22b392e0309abf29de"
        cls.client_auth = Client(headers={
            "Authorization": "Token " + token
        })
        
    def testToken(self):
        
        # Correct details
        response = self.client.post("/auth/token/login/", {
            "username": self.user.username,
            "password": self.data['password']
        })
        self.assertEqual(200, response.status_code)

        # Wrong details
        response = self.client.post("/auth/token/login/", {
            "username": self.user.username,
            "password": "password"
        })
        self.assertEqual(400, response.status_code)
        
    def testRegisterUser(self):
        
        # Same user
        response = self.client.post("/auth/users/", {"username":"test", "password":"testUser12345!"})
        self.assertEqual(400, response.status_code)

        # Different user
        response = self.client.post("/auth/users/", {"username":"test2", "password":"testUser12345!"})
        self.assertNotEqual(400, response.status_code)


