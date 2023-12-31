from django.urls import path
from . import views
from django.contrib.auth.views import *

app_name = 'users'

urlpatterns = [
    path('registration/', views.registration.as_view(), name='registration'),
    path('login/', LoginView.as_view(template_name="users/login.html"), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]
