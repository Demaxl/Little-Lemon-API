import json
from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User, Group

from .models import Category, Cart, CartItem, MenuItem, Order, OrderItem
from .serializers import (MenuItemSerializer, UserSerializer, 
                          CartSerializer, OrderSerializer)
from .permissions import IsManager, IsDeliveryCrew


def userIsManager(user):
    return user.groups.filter(name="Manager").exists()

def userIsDelivery(user):
    return user.groups.filter(name="Delivery Crew").exists()

class MenuItemViewSet(ModelViewSet):
    queryset = MenuItem.objects.select_related("category").all()
    serializer_class = MenuItemSerializer

    pagination_class = PageNumberPagination
    
    search_fields = ["title", "category__title"]
    ordering_fields = ['price']


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


class CartView(generics.ListCreateAPIView):
    # queryset = CartItem.objects.select_related("menu_item")
    queryset = Cart.objects.all()#select_related("menu_items").all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # return CartItem.objects.filter(cart__user=self.request.user)
        return Cart.objects.filter(user=self.request.user)#.select_related("cart_items").all()
    

    def delete(self, request):
        CartItem.objects.filter(cart__user=request.user).delete()
        return Response()

    
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    pagination_class = PageNumberPagination

    search_fields = ["user__username", "delivery_crew__username"]
    ordering_fields = ['status', "date"]


    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.request.method in ["PUT", "DELETE"]:
            permission_classes = [IsManager]

        if self.request.method == "PATCH":
            permission_classes = [IsManager|IsDeliveryCrew]
        return [permission() for permission in permission_classes]
 
    def get_queryset(self):
        orders = Order.objects.select_related("user")
        if userIsManager(self.request.user):
            return orders
        if userIsDelivery(self.request.user):
            return orders.filter(delivery_crew=self.request.user)
        return orders.filter(user=self.request.user)
    
    def retrieve(self, request, pk, *args, **kwargs):
        obj = Order.objects.get(pk=pk)
        if (obj.user != request.user) and (not userIsManager(request.user)):
            raise PermissionDenied(detail="User didnt place this order")
        
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, pk, *args, **kwargs):
        order = Order.objects.get(pk=pk)

        delivery_crew = request.data.get("delivery_crew")
        status_field = request.data.get("status")

        if delivery_crew:
            if userIsDelivery(request.user):
                raise PermissionDenied(detail="You cant set delivery crew")
            try:
                delivery_guy = User.objects.get(username=delivery_crew)
                if not userIsDelivery(delivery_guy):
                    raise User.DoesNotExist
                
                order.delivery_crew = delivery_guy
            except User.DoesNotExist:
                return Response({"delivery_crew":f"{delivery_crew} is not a valid user or part of delivery crew"}, status=status.HTTP_400_BAD_REQUEST)

        if status_field:
            try:
                order.status = json.loads(status_field)
            except json.decoder.JSONDecodeError:
                return Response({"status_field":f"{status_field} must be a boolean field"}, status=status.HTTP_400_BAD_REQUEST)

        order.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
    

    
