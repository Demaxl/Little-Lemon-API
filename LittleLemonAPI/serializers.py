from rest_framework import serializers

from .models import Category, Cart, CartItem, MenuItem, Order, OrderItem
from django.contrib.auth.models import User, Group
from pprint import pprint




class UserSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True)
    class Meta:
        model = User
        fields = ['id', "username", "first_name", "last_name", "email", "groups"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']


class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', "title", "price", "category", "category_id"]

    def __init__(self, *args, **kwargs):
        super(MenuItemSerializer, self).__init__(*args, **kwargs)
        

        # # Check if context has 'exclude_category' set to True
        if self.context.get('exclude_category'):
            self.fields.pop('category')  # Remove the 'category' field from the serializer
    
    def validate_category_id(self, category_id):
        try:
            Category.objects.get(pk=category_id)
            return category_id
        except Category.DoesNotExist:
            raise serializers.ValidationError(f'No category with id {category_id}')


class CartItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(context={"exclude_category":True})
    
    class Meta:
        model = CartItem
        fields = ["quantity", "menu_item"]


class CartSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset = User.objects.all(),
        default=serializers.CurrentUserDefault(),
        slug_field="username")
    
    menu_item = serializers.PrimaryKeyRelatedField(
        queryset = MenuItem.objects.all(),
        write_only = True
    )
    cart_items = CartItemSerializer(many=True, read_only=True)
    items_count = serializers.SerializerMethodField("countItems")
    total_price = serializers.SerializerMethodField("calculateCartPrice")

    class Meta:
        model = Cart
        fields = ['user', "items_count", "total_price", "cart_items", "menu_item"]

    def create(self, validated_data):
        user = validated_data.pop("user")
        menuitem = validated_data.pop("menu_item")
        
        if user.cart.menu_items.contains(menuitem):
            cartitem = user.cart.cart_items.get(menu_item=menuitem)
            cartitem.quantity += 1
            cartitem.save()
        else:
            user.cart.menu_items.add(menuitem)

        user.cart.save()
        return user.cart


    def countItems(self, cart: Cart):
        return len(cart.menu_items.all())

    def calculateCartPrice(self, cart: Cart):
        price = 0

        for cartitem in cart.cart_items.all():
            price += (cartitem.quantity * cartitem.menu_item.price)
        
        return price

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(context={"exclude_category":True})
    
    class Meta:
        model = OrderItem
        fields = ["quantity", "menu_item"]

class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source="id", read_only=True)
    user = serializers.SlugRelatedField(
        queryset = User.objects.all(),
        default=serializers.CurrentUserDefault(),
        slug_field="username")
    
    delivery_crew = serializers.SlugRelatedField(
        queryset = Group.objects.get(name="Delivery Crew").user_set.all(),
        slug_field="username",
        required=False)
    
    total = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    
    order_items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ["order_id","user", "delivery_crew", "status", "total", "date", "order_items"]

    def validate(self, attrs):
        user = attrs['user']

        if user.cart.cart_items.count() == 0:
            raise serializers.ValidationError("User has no items in the cart")
        return super().validate(attrs)

    def create(self, validated_data):
        return super().create(validated_data)