from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter(trailing_slash=False)
router.register("menu-items", views.MenuItemViewSet)


urlpatterns = [
    *router.urls,
    path("groups/<slug:group>/users", views.GroupViewSet.as_view({
        "get": "list",
        "post": "create" }), name="managers"),
    path("groups/<slug:group>/users/<str:username>", views.GroupViewSet.as_view({"delete":"removeUser"}), name="managers"),
    path("cart/menu-items", views.CartView.as_view())


]
