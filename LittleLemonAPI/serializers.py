from rest_framework import serializers

from .models import Category, Cart, CartItem, MenuItem, Order, OrderItem
from django.contrib.auth.models import User, Group




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

    
    def validate_category_id(self, category_id):
        try:
            Category.objects.get(pk=category_id)
            return category_id
        except Category.DoesNotExist:
            raise serializers.ValidationError(f'No category with id {category_id}')
