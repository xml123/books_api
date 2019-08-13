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

#保存或修改文章
#POST
def pushArtical(request):
    if request.method == 'POST':
        data_string = json.loads(request.body)
        try:
            type = data_string['type']
            title = data_string['title']
            content = data_string['content']
            classify_obj = Classify.objects.filter(title=type)
            status = data_string['status']
            fun = data_string['fun']
            localTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            if fun == 'add':
                artical = Artical(title=title, content=content, view=0, status=status, classify_id=classify_obj[0].id,
                              time=localTime)
                artical.save()
            else:
                id = data_string['id']
                artical_obj = Artical.objects.get(id=id)
                artical_obj.title = title
                artical_obj.content = content
                artical_obj.status = status
                artical_obj.save()
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
            artical_list = Artical.objects.filter(classify_id=item1.id, status=True).order_by("-time")
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

#获取指定类型文章
#POST
def getArticalTypeList(request):
    if request.method == 'POST':
        data_string = json.loads(request.body)
        try:
            type = data_string['type']
        except Exception as e:
            print(e)
            print('获取前端传回的数据失败', data_string)
            return
        classify_type = Classify.objects.filter(title=type)
        artical_list = Artical.objects.filter(classify_id=classify_type[0].id, status=True).order_by("-id")
        list = []
        for item in artical_list:
            local_time = item.time
            list.append({
                'id': item.id,
                'title': item.title,
                'content': item.content,
                'view': item.view,
                'type':type,
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

#获取所有文章
#POST
def getAllArtical(request):
    data_string = json.loads(request.body)
    try:
        pageNum = data_string['pageNum']
    except Exception as e:
        print(e)
        print('获取前端传回的数据失败')
    articalList = Artical.objects.filter(status=True).order_by("-time")
    pageSize = 5
    paginator = Paginator(articalList, pageSize)
    total = paginator.count
    all_pages = paginator.num_pages
    if int(pageNum) > all_pages:
        articalList = []
    else:
        try:
            articalList = paginator.page(pageNum)
        except PageNotAnInteger:
            articalList = paginator.page(1)
        except EmptyPage:
            articalList = paginator.page(paginator.num_pages)
    list = []
    for item in articalList:
        local_time = item.time
        classify_type = Classify.objects.filter(id=item.classify_id)
        list.append({
            'id': item.id,
            'title': item.title,
            'content': item.content,
            'view': item.view,
            'time': local_time.strftime('%Y-%m-%d'),
            'type': classify_type[0].type
        })
    data = {
        "code": '200',
        "msg": '成功',
        "data": list,
        "total": total
    }
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json", charset='utf-8', status='200', reason='success')

#删除文章
#POST
def deleatArtical(request):
    if request.method == 'POST':
        data_string = json.loads(request.body)
        try:
            id = data_string['id']
        except Exception as e:
            print(e)
            print('获取前端传回的数据失败')
        artical_obj = Artical.objects.filter(id=id)
        artical_obj.delete()
        data = {
            "code": '200',
            "msg": '成功'
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json", charset='utf-8',
                            status='200', reason='success')
    else:
        return HttpResponse('It is not a POST request!!!')

#获取草稿箱文章
#POST
def getDraftArtical(request):
    if request.method == 'POST':
        data_string = json.loads(request.body)
        try:
            artical_list = Artical.objects.filter(status=False).order_by("-time")
        except Exception as e:
            print(e)
        list = []
        for item in artical_list:
            local_time = item.time
            list.append({
                'id': item.id,
                'title': item.title,
                'content': item.content,
                'view': item.view,
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

#根据id获取文章
#POST
def getArticalId(request):
    if request.method == 'POST':
        data_string = json.loads(request.body)
        try:
            id = data_string['id']
        except Exception as e:
            print(e)
            print('获取前端传回的数据失败')
        artical_obj = Artical.objects.filter(id=id)
        classify_obj = Classify.objects.filter(id=artical_obj[0].classify_id)
        obj = {
            'id': artical_obj[0].id,
            'title': artical_obj[0].title,
            'content': artical_obj[0].content,
            'type': classify_obj[0].title
        }
        data = {
            "code": "200",
            "msg":  "成功",
            "data": obj
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json", charset='utf-8',
                            status='200', reason='success')
    else:
        return HttpResponse('It is not a POST request!!!')

#获取文章评论
#POST
def getArticalMessage(request):
    try:
        data_string = json.loads(request.body)
        id = data_string['id']
    except Exception as e:
        print(e, '获取前端传回的数据失败')
    message_list = ArticalMessage.objects.filter(artical_id=id, parent_comment_id__isnull=True)
    list = []
    for item in message_list:
        local_time = item.created_time
        visitor_obj = Visitor.objects.get(id=item.visitor_id)
        list.append({
            'id': item.id,
            'message': item.message,
            'time': local_time.strftime('%Y-%m-%d'),
            'visitor': {
                'name': visitor_obj.name,
                'id': visitor_obj.id,
                'avatar': visitor_obj.avatar,
                'link': visitor_obj.link
            }
        })
    data = {
        "code": "200",
        "msg": "成功",
        "data": list
    }
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json", charset='utf-8',
                        status='200', reason='success')
#增加文章阅读数
#POST
def addArticalView(request):
    try:
        data_string = json.loads(request.body)
        id = data_string['id']
    except Exception as e:
        print(e, '获取前端传回的数据失败')
    artical_obj = Artical.objects.get(id=id)
    artical_obj.view = artical_obj.view + 1
    artical_obj.save()
    data = {
        "code": "200",
        "msg": "成功",
    }
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json", charset='utf-8',
                        status='200', reason='success')

#添加评论
#POST
def addArticalMessage(request):
    try:
        data_string = json.loads(request.body)
        artical_id = data_string['artical_id']
        message = data_string['message']
        user_id = data_string['user_id']
        localTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    except Exception as e:
        print(e, '获取前端传回的数据失败')
    message_obj = ArticalMessage(message=message, artical_id=artical_id, visitor_id=user_id, time=localTime,
                                 parent_comment_id=False)
    message_obj.save()
    data = {
        "code": "200",
        "msg": "成功"
    }
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json", charset='utf-8',
                        status='200', reason='success')


