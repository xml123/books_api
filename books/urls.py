from django.urls import path
from . import views

app_name = 'books'
urlpatterns = [
	path('api/get_all_books', views.getAllBooks, name='getAllBooks'),					#查询所有书籍
	path('api/get_you_like', views.getYouLike, name='getYouLike'),						#猜你喜欢
	path('api/get_hot_recommend', views.getHotRecommend, name='getHotRecommend'),		#热门推荐
	path('api/get_chapter', views.getChapter, name='getChapter'),						#小说章节
	path('api/get_chapter_detail', views.getChapterDetail, name='getChapterDetail'),	#小说章节详情
	path('api/get_abstract', views.getAbstract, name='getAbstract'),					#小说简介
	path('api/get_banner_one', views.getBannerOne, name='getBannerOne'),				#首页banner推荐
]