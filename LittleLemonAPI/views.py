from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.decorators import action

from django.contrib.auth.models import User, Group
from .models import Category, Cart, CartItem, MenuItem, Order, OrderItem
from .serializers import MenuItemSerializer, UserSerializer, CategorySerializer
from .permissions import IsManager


class MenuItemViewSet(ModelViewSet):
    queryset = MenuItem.objects.select_related("category").all()
    serializer_class = MenuItemSerializer


    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsManager]
                
        return [permission() for permission in permission_classes]


class GroupViewSet(ViewSet):
    permission_classes = [IsManager]

    def list(self, request, group):
        group = group.replace("-", " ")
        queryset = get_object_or_404(Group, name__iexact=group).user_set.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    

    def create(self, request, group):
        username = request.data.get("user")
        group = group.replace("-", " ")

        
        if username:
            user = get_object_or_404(User, username=username)
            group = get_object_or_404(Group, name__iexact=group)
            user.groups.add(group)
            user.save()
            return Response({"success":"ok"}, status=status.HTTP_201_CREATED)

        else:
            return Response({"detail":"username not specified"}, status=status.HTTP_400_BAD_REQUEST)

    def removeUser(self, request, group, username):
        group = group.replace("-", " ")
        user = get_object_or_404(User, username=username)
        manager = get_object_or_404(Group, name__iexact=group)
        user.groups.remove(manager)

        return Response(status=status.HTTP_204_NO_CONTENT)



