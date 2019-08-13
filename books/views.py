from django.shortcuts import render, get_object_or_404
import json
import random

# Create your views here.
from django.http import HttpResponse
from .models import Author, Category, Book, chapter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from users.models import Users,BookCapter

#获取所有书籍信息
#@methord:POST
#@pageNum:页码
#@pageSize:每页数据总数
def getAllBooks(request):
	if request.method == 'POST':
		data_string = request.POST
		try:
			pageNum = data_string['pageNum']
			pageSize = data_string['pageSize']
		except Exception as e:
			print(e)
			print('获取前端传回的数据失败')
		book_list = Book.objects.all().order_by('id')
		paginator = Paginator(book_list, pageSize)
		total = paginator.count
		all_pages = paginator.num_pages
		if int(pageNum) > all_pages:
			books = []
		else:
			try:
				books = paginator.page(pageNum)
			except PageNotAnInteger:
				books = paginator.page(1)
			except EmptyPage:
				books = paginator.page(paginator.num_pages)

		arrayList = []
		for item in books:
			book_id = item.id
			book_detail = Book.objects.filter(id=book_id)
			arrayList.append({
				'id':item.id,
				'title':item.title,
				'author':item.author.name,		#关联表查询
				'category':item.category.name,
				'bookImg':item.book_img,
				'abstract':book_detail[0].book_abstract
				})

		data = {
			"code":'200',
			"msg":'成功',
			"data":arrayList,
			"total":total
		}
		return HttpResponse(json.dumps(data,ensure_ascii=False), content_type="application/json", charset='utf-8',status='200',reason='success')
	else:
		return HttpResponse('It is not a POST request!!!')

#猜你喜欢
#@methord GET
def getYouLike(request):
	num_list = range(1,30)
	result = random.sample(num_list, 3)
	book_list = Book.objects.filter(id__in=result) 
	arrayList = []

	for item in book_list:
		arrayList.append({
			'id':item.id,
			'title':item.title,
			'author':item.author.name,		#关联表查询
			'category':item.category.name,
			'bookImg':item.book_img,
			})
	data = {
		"code":'200',
		"msg":'成功',
		"data":arrayList
	}
	return HttpResponse(json.dumps(data,ensure_ascii=False), content_type="application/json", charset='utf-8', status='200',reason='success')

#热门推荐
#@methord GET
def getHotRecommend(request):
	num_list = range(30,100)
	result = random.sample(num_list, 6)
	try:
		book_list = Book.objects.filter(id__in=result)
	except Exception as e:
		print('查询数据失败！')
		return ''
	arrayList = []
	for item in book_list:
		arrayList.append({
			'id':item.id,
			'title':item.title,
			'author':item.author.name,		#关联表查询
			'category':item.category.name,
			'bookImg':item.book_img,
			})
	data = {
		"code":'200',
		"msg":'成功',
		"data":arrayList
	}
	return HttpResponse(json.dumps(data,ensure_ascii=False), content_type="application/json", charset='utf-8', status='200',reason='success')

#获取小说所有章节
#@methord POST
#@id	小说id
def getChapter(request):
	if request.method == 'POST':
		data_string = request.POST
		try:
			book_id = data_string['id']
		except Exception as e:
			print(e)
			print('获取前端传回的数据失败')
		chapter_list = chapter.objects.filter(book_id_id=book_id)
		chapterList = []
		for item in chapter_list:
			chapterList.append({
				'book_id':book_id,
				'id':item.chapter_id,
				'chapter_title':item.name,
				})
		data = {
			"code":'200',
			"msg":'成功',
			"data":chapterList
		}
		return HttpResponse(json.dumps(data,ensure_ascii=False), content_type="application/json", charset='utf-8',status='200',reason='success')
	else:
		return HttpResponse('It is not a POST request!!!')

#获取小说某一章的数据
#@methord POST
#@bookId 	小说id
#@chapterId 	章节id
def getChapterDetail(request):
	if request.method == 'POST':
		data_string = request.POST
		try:
			book_id = data_string['bookId']
			chapter_id = data_string['chapterId']
		except Exception as e:
			print(e)
			print('获取前端传回的数据失败')
		chapter_detail = chapter.objects.filter(book_id_id=book_id, chapter_id=chapter_id)
		print
		data = {
			"code":'200',
			"msg":'成功',
			"data":{
				"content":chapter_detail[0].chapter_text,
				"book_id":book_id,
				"title":chapter_detail[0].name
			}
		}

		return HttpResponse(json.dumps(data,ensure_ascii=False), content_type="application/json", charset='utf-8',status='200',reason='success')
	else:
		return HttpResponse('It is not a POST request!!!')

#获取小说简介
#@methord 	POST
#@bookId 	小说id
#@openid 	用户openid
def getAbstract(request):
	if request.method == 'POST':
		data_string = request.POST
		try:
			book_id = data_string['bookId']
			openid = data_string['openId']
		except Exception as e:
			print(e)
			print('获取前端传回的数据失败')
			return
		book_detail = Book.objects.filter(id=book_id)
		user_obj = Users.objects.get(openid=openid)
		books = user_obj.book.filter(id=book_id)
		userid = Users.objects.filter(openid=openid)
		chapter_obj = BookCapter.objects.filter(bookid=book_id,users_id=userid[0].id)
		if len(books):
			user_chapter = chapter_obj[0].capterid
			print('user_chapter',user_chapter)
		else:
			user_chapter = 1
		data = {
			"code":200,
			"msg":'成功',
			"data":{
				"title":book_detail[0].title,
				"author":book_detail[0].author.name,
				"image":book_detail[0].book_img,
				"category":book_detail[0].category.name,
				"abstract":book_detail[0].book_abstract,
				"collect":len(books),	#该用户是否收藏该书 0:否，1：是
				"chapterid":user_chapter
			}
		}

		return HttpResponse(json.dumps(data,ensure_ascii=False), content_type="application/json", charset='utf-8',status='200',reason='success')
	else:
		return HttpResponse('It is not a POST request!!!')

#首页banner推荐
#@methord GET
def getBannerOne(request):
	#第一张banner数据
	try:
		book = Book.objects.filter(id = 10)
		bannerOne = {
			"id":book[0].id,
			"title":book[0].title,
			"bookImg":book[0].book_img,
			"author":book[0].author.name,
		}
	except:
		print('获取书籍出错')
		return
	#第二张banne数据
	try:
		books = Book.objects.all()[5:11]
	except:
		print('获取书籍出错')
		return
	bannerTwo = []
	for item in books:
		bannerTwo.append({
			'id':item.id,
			'title':item.title,
			'author':item.author.name,		#关联表查询
			'bookImg':item.book_img,
			})

	data = {
		"code":200,
		"msg":'成功',
		"data":{
			"bannerOne":bannerOne,
			"bannerTwo":bannerTwo
		}
	}
	return HttpResponse(json.dumps(data,ensure_ascii=False), content_type="application/json", charset='utf-8', status='200',reason='success')









