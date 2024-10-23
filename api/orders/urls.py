from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import OrdersViewSet, PromotionalCodeViewSet

router = DefaultRouter()
router.register('orders', OrdersViewSet)  # Добавляем префикс 'orders'
router.register('promotional-codes', PromotionalCodeViewSet)  # Здесь префикс 'promotional-codes'

urlpatterns = [
    path('', include(router.urls))
]
