from django.urls import path
from . import views

app_name = 'bloag'

urlpatterns = [
    path('api/get_friends', views.getFriends, name='getFriends'),
    path('api/get_head_list', views.getHeaderList, name='getHeaderList'),
    path('api/push_artical', views.pushArtical, name='pushArtical'),
    path('api/get_artical_list', views.getArticalList, name='getArticalList')
]