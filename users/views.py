from django.shortcuts import render, get_object_or_404
import json

# Create your views here.
from django.http import HttpResponse
from .models import Users,BookCapter,UserReadStatus
from django.core import serializers
import requests
from books.models import Author, Category, Book, chapter
import urllib.request
import urllib.parse
#解析微信返回的数据
# def process_response_login(rsp):
# 	print('rsp',rsp.read().decode('utf-8'))
# 	"""解析微信登录返回的json数据，返回相对应的dict, 错误信息"""
# 	if 200 != rsp.status_code:
# 		return None, {'code': rsp.status_code, 'msg': 'http error'}
# 	try:
# 		content = rsp.json()
# 	except Exception as e:
# 		return None, {'code': 9999, 'msg': e}
# 	if 'errcode' in content and content['errcode'] != 0:
# 		return None, {'code': content['errcode'], 'msg': content['errmsg']}
# 	return content, None

def process_response_login(rsp):
	try:
		#content2 = rsp.read().decode('utf-8')
		content = rsp.json()
	except Exception as e:
		print('出错了')
		return None, {'code': 9999, 'msg': e}
	if 'errcode' in content and content['errcode'] != 0:
		return None, {'code': content['errcode'], 'msg': content['errmsg']}
	return content, None

#获取openid
def getWxAppid(code):
	s = requests.Session()
	params = {
            'appid': 'wxff782f9a8a041250',
            'js_code': code,
            'secret': '73515868baa360f1dbe6caa0d50b0e6b',
            'grant_type':'authorization_code'
            }
	url = 'https://api.weixin.qq.com/sns/jscode2session?appid=wxff782f9a8a041250&js_code=%s&secret=73515868baa360f1dbe6caa0d50b0e6b&grant_type=authorization_code' % code
    #token, err = process_response_login(requests.get('https://api.weixin.qq.com/sns/jscode2session', params=params))
	# token, err = process_response_login(urllib.request.urlopen(url))
	token, err = process_response_login(s.get(url))
	if not err:
		_session_key = token['session_key']
		_openid = token['openid']
		is_user = Users.objects.filter(openid=_openid)
		if not is_user:		#判断是否已存在该用户
			user = Users(openid=_openid,session_key=_session_key,code=code)
			user.save()		#保存该用户到数据库
	return _openid

#前端请求数据
#@methord POST
#@code 用户code
def getAuth(request):
	if request.method == 'POST':
		code_string = request.POST
		code = code_string['code'] #获取前端传过来的code值
		#print ('message2',code)
		openid = getWxAppid(code)
		received_json_data = {
			'code':200,
			'openid':openid
		}
		return HttpResponse(json.dumps(received_json_data,ensure_ascii=False), content_type="application/json;charset = utf-8", charset='utf-8')
	else:
		return HttpResponse('It is not a POST request!!!')

#保存收藏
#@methord POST
#@openid 用户openid
#@bookid 书id
def saveCollectBook(request):
	if request.method == 'POST':
		data_string = request.POST
		try:
			openid = data_string['openid']
			bookid = data_string['bookid']
			book_obj = Book.objects.get(id=bookid)
			user_obj = Users.objects.get(openid=openid)
			user_obj.book.add(book_obj)
		except Exception as e:
			print('获取前端传回的数据失败')
			print(e)

		data = {
			"code":200,
			"msg":'成功',
		}
		return HttpResponse(json.dumps(data,ensure_ascii=False), content_type="application/json", charset='utf-8',status='200',reason='success')
	else:
		return HttpResponse('It is not a POST request!!!')

#移除该书的收藏
#@method 	POST
#@openid 用户openid
#@bookid 书id
def removeCollectBook(request):
	if request.method == 'POST':
		data_string = request.POST
		try:
			openid = data_string['openid']
			bookid = data_string['bookid']
			book_obj = Book.objects.get(id=bookid)
			user_obj = Users.objects.get(openid=openid)
			userid = Users.objects.filter(openid=openid)
			chapter_obj = BookCapter.objects.filter(bookid=bookid,users_id=userid[0].id)
			chapter_obj.delete()	#删除记录的章节
			user_obj.book.remove(book_obj)
		except Exception as e:
			print('获取前端传回的数据失败')
			print(e)

		data = {
			"code":200,
			"msg":'成功'
		}
		return HttpResponse(json.dumps(data,ensure_ascii=False), content_type="application/json", charset='utf-8',status='200',reason='success')
	else:
		return HttpResponse('It is not a POST request!!!')

#我的收藏
#@methord POST
#@openid 用户openid
def getCollect(request):
	if request.method == 'POST':
		data_string = request.POST
		try:
			openid = data_string['openid']
			user_obj = Users.objects.get(openid=openid)
			books = user_obj.book.all()
			userid = Users.objects.filter(openid=openid)
			arrayList = []
			for item in books:
				chapter_obj = BookCapter.objects.filter(bookid=item.id,users_id=userid[0].id)
				if len(chapter_obj):
					user_chapter = chapter_obj[0].capterid
				else:
					user_chapter = 1
				arrayList.append({
					'id':item.id,
					'title':item.title,
					'author':item.author.name,		#关联表查询
					'category':item.category.name,
					'bookImg':item.book_img,
					"chapterid":user_chapter
					})
		except Exception as e:
			print('获取前端传回的数据失败')
			print(e)

		data = {
			"code":200,
			"msg":'成功',
			"data":arrayList
		}
		return HttpResponse(json.dumps(data,ensure_ascii=False), content_type="application/json", charset='utf-8',status='200',reason='success')
	else:
		return HttpResponse('It is not a POST request!!!')

#保存看到的章节
#@methord 	POST
#@openid 	用户id
#@bookid 	书id
#@capterid 	章节id
def saveChapter(request):
	if request.method == 'POST':
		data_string = request.POST
		try:
			openid = data_string['openid']
			bookid = data_string['bookid']
			capterid = data_string['capterid']

			userid = Users.objects.filter(openid=openid)
			is_bookid = BookCapter.objects.filter(bookid=bookid,users_id=userid[0].id)
			if not is_bookid:
				print('新保存成功')
				bookCapter = BookCapter(users_id=userid[0].id,bookid=bookid,capterid=capterid)
				bookCapter.save()
			else:
				print('更新成功')
				this_book = BookCapter.objects.get(bookid=bookid)
				this_book.capterid = capterid
				this_book.save()
		except Exception as e:
			print(e)
			return HttpResponse('获取前端传回的数据失败')
		data = {
			"code":200,
			"msg":'成功',
		}
		return HttpResponse(json.dumps(data,ensure_ascii=False), content_type="application/json", charset='utf-8',status='200',reason='success')
	else:
		return HttpResponse('It is not a POST request!!!')

#保存用户的阅读习惯
#@method 	POST
#@openid 	string 用户id
#@read_status string 阅读模式 0:日间	1:夜间	@选填
#@word_size string 字体大小	@选填
#bg_color string 背景颜色 @选填

def saveUsetSetting(request):
	if request.method == 'POST':
		data_string = request.POST
		try:
			openid = data_string['openid']
			if not data_string['read_status']:
				read_status = '0'
			else:
				read_status = data_string['read_status']
			if not data_string['word_size']:
				word_size = '32'
			else:
				word_size = data_string['word_size']
			if not data_string['bg_color']:
				bg_color = '#fff'
			else:
				bg_color = data_string['bg_color']

			userid = Users.objects.filter(openid=openid)
			setting_obj = UserReadStatus.objects.filter(users_id=userid[0].id)
			if not setting_obj:
				status_obj = UserReadStatus(users_id=userid[0].id,read_status=read_status,word_size=word_size,bg_color=bg_color)
			else:
				status_obj = UserReadStatus.objects.get(users_id=userid[0].id)
				status_obj.read_status = read_status
				status_obj.word_size = word_size
				status_obj.bg_color = bg_color
			status_obj.save()		#保存该用户到数据库

		except Exception as e:
			print('获取前端传回的数据失败')
			print(e)

		data = {
			"code":200,
			"msg":'成功',
		}
		return HttpResponse(json.dumps(data,ensure_ascii=False), content_type="application/json", charset='utf-8',status='200',reason='success')
	else:
		return HttpResponse('It is not a POST request!!!')

#获取用户小说设置
#@method 	POST
def getUsetSetting(request):
	if request.method == 'POST':
		data_string = request.POST
		try:
			openid = data_string['openid']
			userid = Users.objects.filter(openid=openid)
			setting_obj = UserReadStatus.objects.filter(users_id=userid[0].id)

			data_str = {
				'read_status':setting_obj[0].read_status,
				'word_size':setting_obj[0].word_size,
				'bg_color':setting_obj[0].bg_color
			}

		except Exception as e:
			print('获取前端传回的数据失败')
			print(e)
		data = {
			"code":200,
			"msg":'成功',
			"data":data_str
		}
		return HttpResponse(json.dumps(data,ensure_ascii=False), content_type="application/json", charset='utf-8',status='200',reason='success')
	else:
		return HttpResponse('It is not a POST request!!!')







