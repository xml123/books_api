from django.urls import path
from . import views

app_name = 'equitysys'

urlpatterns = [
    path('api/equity/login', views.login, name='login')
]