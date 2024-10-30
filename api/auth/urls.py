from django.urls import  path,include
from rest_framework.routers import DefaultRouter
from .views import  *

router = DefaultRouter()
router.register('profile',ProfileViewSet)

urlpatterns = [
    # ChangPassword
    path('register/',RegisterAPIView.as_view()),
    path('login/',LoginAPIView.as_view()),
    path('chang-password/',ChangPassword.as_view()),
    path('',include(router.urls))
]