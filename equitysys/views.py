from django.shortcuts import render, get_object_or_404
import json
from django.http import HttpResponse, HttpResponseRedirect
from .models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import time
import requests
#import qrcode
from datetime import datetime

# Create your views here.
#POST
def login(request):
    if request.method == 'POST':
        data_string = json.loads(request.body)
        try:
            name = data_string['username']
            password = data_string['password']
        except Exception as e:
            print('获取前端传回的数据失败',e)
            return
        user_obj = User.objects.filter(name=name, password=password)
        if(len(user_obj) > 0):
            data = {
                "code": 200,
                "data": {
                    "message": '成功',
                    "status": "ok"
                }
            }
        else:
            data = {
                "code": 200,
                "data": {
                    "message": '用户名或密码错误',
                    "status": "fail"
                }
            }
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json", charset='utf-8',
                            status='200', reason='success')