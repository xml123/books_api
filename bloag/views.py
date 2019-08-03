from django.shortcuts import render, get_object_or_404
import json
from django.http import HttpResponse
from .models import Classify, Visitor, Artical, ArticalMessage,LiveMessage,Friends
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import time
from datetime import datetime

# Create your views here.
#获取友情链接
#GET
def getFriends(request):
    friends = Friends.objects.all()
    arrayList = []
    for item in friends:
        arrayList.append({
            'id': item.id,
            'name': item.name,
            'avatar': item.avatar,
            'link': item.link,
            'abstract': item.abstract
        })
    data = {
        "code": '200',
        "msg": '成功',
        "data": arrayList,
    }
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json", charset='utf-8', status='200', reason='success')

#获取头部标签
#POST
def getHeaderList(request):
    if request.method == 'POST':
        data_string = json.loads(request.body)
        try:
            type = data_string['type']
        except Exception as e:
            print(e)
            print('获取前端传回的数据失败', data_string)
            return
        types = Classify.objects.filter(type=type)
        typeList = []
        for item in types:
            typeList.append({
                'id': item.id,
                'title': item.title,
                'type': item.type
            })

        data = {
            "code": '200',
            "msg": '成功',
            "data": typeList,
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json", charset='utf-8',
                            status='200', reason='success')
    else:
        return HttpResponse('It is not a POST request!!!')

#发布文章
#POST
def pushArtical(request):
    if request.method == 'POST':
        data_string = json.loads(request.body)
        try:
            type = data_string['type']
            title = data_string['title']
            content = data_string['content']
            classify_obj = Classify.objects.filter(title=type)
            print('classify_obj', classify_obj)
            localTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            artical = Artical(title=title, content=content, view=0, status=False, classify_id=classify_obj[0].id,
                              time=localTime)
            artical.save()

        except Exception as e:
            print(e)
            print('获取前端传回的数据失败', data_string)
        data = {
            "code": 200,
            "msg": '成功',
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json", charset='utf-8',
                            status='200', reason='success')
    else:
        return HttpResponse('It is not a POST request!!!')

#获取文章列表
#POST
def getArticalList(request):
    if request.method == 'POST':
        data_string = json.loads(request.body)
        try:
            type = data_string['type']
        except Exception as e:
            print(e)
            print('获取前端传回的数据失败', data_string)
            return
        classify_type = Classify.objects.filter(type=type)
        list = []
        for item1 in classify_type:
            artical_list = Artical.objects.filter(classify_id=item1.id)
            for item in artical_list:
                local_time = item.time
                list.append({
                    'id': item.id,
                    'title': item.title,
                    'time': local_time.strftime('%Y-%m-%d')
                })

        data = {
            "code": '200',
            "msg": '成功',
            "data": list,
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json", charset='utf-8',
                            status='200', reason='success')
    else:
        return HttpResponse('It is not a POST request!!!')


