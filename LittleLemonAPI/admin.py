from django.contrib import admin
from .models import Category, Cart, CartItem, MenuItem, Order, OrderItem

# Register your models here.
admin.site.register(Category)
admin.site.register(CartItem)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderItem)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    filter_horizontal = ("menu_items",)