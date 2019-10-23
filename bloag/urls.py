from django.urls import path
from . import views

app_name = 'bloag'

urlpatterns = [
    path('api/get_friends', views.getFriends, name='getFriends'),
    path('api/get_head_list', views.getHeaderList, name='getHeaderList'),
    path('api/push_artical', views.pushArtical, name='pushArtical'),
    path('api/get_artical_list', views.getArticalList, name='getArticalList'),
    path('api/get_artical_type_list', views.getArticalTypeList, name='getArticalTypeList'),
    path('api/get_all_artical', views.getAllArtical, name='getAllArtical'),
    path('api/delete_artical', views.deleatArtical, name='deleatArtical'),
    path('api/get_draft_artical', views.getDraftArtical, name='getDraftArtical'),
    path('api/get_artical_id', views.getArticalId, name='getArticalId'),
    path('api/get_artical_message', views.getArticalMessage, name='getArticalMessage'),
    path('api/add_artical_view', views.addArticalView, name='addArticalView'),
    path('api/add_artical_message', views.addArticalMessage, name='addArticalMessage'),
    path('api/get_code', views.getCode, name='getCode'),
    path('api/get_live_message', views.getLiveMessage, name='getLiveMessage'),
    path('api/add_live_message', views.addLiveMessage, name='addLiveMessage'),
    path('api/get_openid', views.getOpenid, name='getOpenid'),
    path('api/get_wechat_code', views.getWechatCode, name='getWechatCode'),
    path('api/get_wechat_message', views.getWechatMessage, name='getWechatMessage')
]
