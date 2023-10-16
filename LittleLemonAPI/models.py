from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True)


class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    featured = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="menu_items")

    class Meta:
        indexes = [models.Index(fields=["price", "title", "featured"])]

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    items_count = models.PositiveSmallIntegerField()
    total_price = models.DecimalField(max_digits=6, decimal_places=2)()
    menu_items = models.ManyToManyField(
        MenuItem, 
        through="CartItem", 
        through_fields=("cart", "menu_item"))

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveSmallIntegerField()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    delivery_crew = models.ForeignKey(User, on_delete=models.SET("Resigned"), related_name="delivery_crew", null=True)
    status = models.BooleanField(default=0)
    total = models.DecimalField(max_digits=6, decimal_places=2)   
    date = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveSmallIntegerField()
