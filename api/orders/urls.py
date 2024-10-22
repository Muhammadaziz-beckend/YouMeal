from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import  OrdersViewSet

router = DefaultRouter()
router.register('',OrdersViewSet)


urlpatterns = [
     path('',include(router.urls))
]