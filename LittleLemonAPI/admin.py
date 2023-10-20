from typing import Any
from django.contrib import admin
from .models import Category, Cart, CartItem, MenuItem, Order, OrderItem

# Register your models here.
admin.site.register(Category)
admin.site.register(CartItem)
admin.site.register(MenuItem)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    filter_horizontal = ("menu_items",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ("total",)

    def get_form(self, request: Any, obj: Any | None = ..., change: bool = ..., **kwargs: Any) -> Any:
        form = super().get_form(request, obj, change, **kwargs)

        if change:
            form.base_fields['user'].disabled = True

        return form



@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    readonly_fields = ("order", "menu_item", "quantity")


