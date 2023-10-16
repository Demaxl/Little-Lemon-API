from django.contrib.auth.models import User, Group
from django.test import Client

import random

users = ["hermione", "ron", "jimmydoe", "johndoe", "adrian", "sana", "mario", "david"]
groups = [Group.objects.get(name="Manager"), Group.objects.get(name="Delivery Crew")]


c = Client()

for user in users:
    response = c.post("/auth/token/login/", {"username":user, "password":"Characters12345!"})
    print(response.status_code)

    