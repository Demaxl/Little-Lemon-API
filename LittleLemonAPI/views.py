from django.shortcuts import render
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from .models import Category, Cart, CartItem, MenuItem, Order, OrderItem
from .serializers import MenuItemSerializer
from .permissions import IsManager


class MenuItemViewSet(ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsManager]
                
        return [permission() for permission in permission_classes]



