from django.urls import  path,include
from .yaml import urlpatterns as swagger
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products',ProductViewSet)
router.register('category',CategoryViewSet)
router.register('orders',OrdersViewSet)

urlpatterns = [
    path('auth/',include('api.auth.urls')),
    path('orders/',include('api.orders.urls')),
    path('',include(router.urls))
]

urlpatterns += swagger