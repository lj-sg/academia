from django.urls import path
from . import views
from .views import profile_view

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', profile_view, name='user_profile'),
]
