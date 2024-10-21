from django.urls import  path,include
from rest_framework.routers import DefaultRouter
from .views import  *

router = DefaultRouter()
router.register('profile',ProfileViewSet)

urlpatterns = [
    path('register/',RegisterAPIView.as_view()),
    path('login/',LoginAPIView.as_view()),
    path('',include(router.urls))
]