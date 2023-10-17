from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter(trailing_slash=False)
router.register("menu-items", views.MenuItemViewSet)

urlpatterns = router.urls
