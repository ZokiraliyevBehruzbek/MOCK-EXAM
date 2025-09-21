from django.urls import path
from users.views import RegisterAPIView,GetMe,LoginAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register_post'),
    path("me/", GetMe.as_view(), name='get_me'),
    path('login/', LoginAPIView.as_view(), name='login'),

]
