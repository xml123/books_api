from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
	path('api/get_auth', views.getAuth, name='getAuth'),
	path('api/save_collect_book', views.saveCollectBook, name='saveCollectBook'),	#保存收藏
	path('api/get_collect', views.getCollect, name='getCollect'),	#获取收藏
	path('api/save_chapter', views.saveChapter, name='saveChapter'),	#保存看到的章节
	path('api/remove_collect_book', views.removeCollectBook, name='removeCollectBook'),	#移除收藏的该书
	path('api/save_user_setting', views.saveUsetSetting, name='saveUsetSetting'),	#移除收藏的该书
	path('api/get_user_setting', views.getUsetSetting, name='getUsetSetting'),	#移除收藏的该书
]