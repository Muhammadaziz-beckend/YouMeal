from django.urls import  path,include
from rest_framework.routers import DefaultRouter
from .views import  *
from .viewsOrdersAndHisory import  *

router = DefaultRouter()
router.register('profile', ProfileViewSet, basename='user-profile')
router.register('order', OrdersViewSet, basename='order')
router.register('history', HistoryViewSet, basename='user-history')

urlpatterns = [
    path('register/',RegisterAPIView.as_view()),
    path('login/',LoginAPIView.as_view()),
    path('chang-password/',ChangPassword.as_view()),
    path('logout/', LogoutApiView.as_view()),
    path('',include(router.urls))
]