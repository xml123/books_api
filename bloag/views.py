from django.shortcuts import render, get_object_or_404
import json
from django.http import HttpResponse
from .models import Classify, Visitor, Artical, ArticalMessage,LiveMessage,Friends
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
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
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json", charset='utf-8', status='200', reason='success')
    else:
        return HttpResponse('It is not a POST request!!!')



