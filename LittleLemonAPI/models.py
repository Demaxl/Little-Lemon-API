from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True)

    def __str__(self) -> str:
        return self.title
    
class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(1)])
    featured = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="menu_items")

    def __str__(self):
        return self.title

    
    class Meta:
        indexes = [models.Index(fields=["price", "title", "featured"])]

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart", primary_key=True)
    menu_items = models.ManyToManyField(
        MenuItem, 
        through="CartItem", 
        through_fields=("cart", "menu_item"))
    
    def __str__(self) -> str:
        return f"{self.user}'s cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self) -> str:
        return f"{self.menu_item} in {self.cart}"

    class Meta:
        unique_together = ["cart", "menu_item"]



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    delivery_crew = models.ForeignKey(User, on_delete=models.SET("Resigned"), related_name="delivery_crew", null=True)
    status = models.BooleanField(default=0)
    total = models.DecimalField(max_digits=6, decimal_places=2)   
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Order by {self.user}"

    class Meta:
        indexes = [models.Index(fields=['status', 'date'])]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    def __str__(self) -> str:
        return f"Order Item in {self.user}'s order"
    

"""
from LittleLemonAPI.models import *
from LittleLemonAPI.serializers import * 
from django.contrib.auth.models import User, Group
user = User.objects.get(username="sana")
"""