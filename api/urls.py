from django.urls import  path,include
from .yaml import urlpatterns as swagger
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products',ProductViewSet)
router.register('category',CategoryViewSet)

urlpatterns = [
    path('',include(router.urls))
]

urlpatterns += swagger