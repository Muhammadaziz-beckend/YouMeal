from django.urls import  path,include
from rest_framework.routers import DefaultRouter

from .views import CardsViewSet

router = DefaultRouter()
router.register('cards',CardsViewSet)

urlpatterns = [
    path('',include(router.urls))
]