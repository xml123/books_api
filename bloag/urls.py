from django.urls import path
from . import views

app_name = 'bloag'

urlpatterns = [
    path('api/get_friends', views.getFriends, name='getFriends'),
    path('api/get_head_list', views.getHeaderList, name='getHeaderList'),
]