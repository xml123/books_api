from django.urls import path
from . import views

app_name = 'equitysys'

urlpatterns = [
    path('api/equity/user', views.login, name='login')
]