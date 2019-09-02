from django.shortcuts import render, get_object_or_404
import json
from django.http import HttpResponse
from .models import Classify, Visitor, Artical, ArticalMessage, LiveMessage, Friends
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import time
import requests
#import qrcode
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
            content_text = data_string['contentText']
            localTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            if fun == 'add':
                artical = Artical(title=title, content=content, content_text=content_text, view=0, status=status, classify_id=classify_obj[0].id,
                              time=localTime)
                artical.save()
            else:
                id = data_string['id']
                artical_obj = Artical.objects.get(id=id)
                artical_obj.content_text = content_text
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
                'type': type,
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
            'type': classify_type[0].type,
            'classType': classify_type[0].title,
            'contentText': item.content_text
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
    message_list = ArticalMessage.objects.filter(artical_id=id, parent_comment_id__isnull=True).order_by("-created_time")
    list = []
    for item in message_list:
        local_time = item.created_time
        visitor_obj = Visitor.objects.get(id=item.visitor_id)
        message_item_id = item.id
        child_message_list = ArticalMessage.objects.filter(artical_id=id, parent_comment_id=message_item_id).order_by("-created_time")
        child_list = []
        for item2 in child_message_list:
            local_time2 = item2.created_time
            visitor_obj2 = Visitor.objects.get(id=item2.visitor_id)
            child_list.append({
                'id': item2.id,
                'message': item2.message,
                'time': local_time2.strftime('%Y-%m-%d'),
                'visitor': {
                    'name': visitor_obj2.name,
                    'id': visitor_obj2.id,
                    'avatar': visitor_obj2.avatar,
                    'link': visitor_obj2.link
                }
            })
        list.append({
            'id': message_item_id,
            'message': item.message,
            'time': local_time.strftime('%Y-%m-%d'),
            'visitor': {
                'name': visitor_obj.name,
                'id': visitor_obj.id,
                'avatar': visitor_obj.avatar,
                'link': visitor_obj.link
            },
            'child_message_list': child_list
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
        message = data_string['comment']
        user_name = data_string['name']
        localTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        user_obj = Visitor.objects.get(name=user_name)
        replay_id = data_string['replay_id']
    except Exception as e:
        print(e, '获取前端传回的数据失败')
    if replay_id == '':
        message_obj = ArticalMessage(message=message, artical_id=artical_id, visitor_id=user_obj.id,
                                     created_time=localTime)
    else:
        message_obj = ArticalMessage(message=message, artical_id=artical_id, visitor_id=user_obj.id,
                                     created_time=localTime, parent_comment_id=replay_id)
    message_obj.save()
    data = {
        "code": "200",
        "msg": "成功"
    }
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json", charset='utf-8',
                        status='200', reason='success')

#github登录
#POST
def getCode(request):
    try:
        data_string = json.loads(request.body)
        code = data_string['code']
        post_data = {'code': code, 'client_id': '0fd0f7869375ba937215', 'client_secret': '8fbbd77ad452b730cdd4912dc9646bf33a602abf'}
        response = requests.post('https://github.com/login/oauth/access_token', data=post_data)
        content = response.content
        json_str = content.decode()
        json_data = json_str.split('=')
        access_token = json_data[1]
        json_data2 = access_token.split('&')
        access_token2 = json_data2[0]

        #获取用户基本信息
        response2 = requests.get('https://api.github.com/user', {'access_token': access_token2})
        content2 = response2.content
        res_str = content2.decode()
        req_data = json.loads(res_str)
        resp_data = {
            "name": req_data['login'],
            "avatar_url": req_data['avatar_url'],
            "html_link": req_data['html_url']
        }
        user_obj = Visitor.objects.filter(name=req_data['login'])
        if not user_obj:
            user = Visitor(name=req_data['login'], avatar=req_data['avatar_url'], link=req_data['html_url'])
            user.save()
        print('res_str', )
    except Exception as e:
        print(e, '获取前端传回的数据失败')

    data = {
        "code": "200",
        "msg": "成功",
        "data": resp_data
    }
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json", charset='utf-8',
                        status='200', reason='success')

#获取留言
#GET
def getLiveMessage(request):
    message_list = LiveMessage.objects.filter(parent_comment_id__isnull=True).order_by("-created_time")
    list = []
    for item in message_list:
        local_time = item.created_time
        visitor_obj = Visitor.objects.get(id=item.visitor_id)
        message_item_id = item.id
        child_message_list = LiveMessage.objects.filter(parent_comment_id=message_item_id).order_by("-created_time")
        child_list = []
        for item2 in child_message_list:
            local_time2 = item2.created_time
            visitor_obj2 = Visitor.objects.get(id=item2.visitor_id)
            child_list.append({
                'id': item2.id,
                'message': item2.message,
                'time': local_time2.strftime('%Y-%m-%d'),
                'visitor': {
                    'name': visitor_obj2.name,
                    'id': visitor_obj2.id,
                    'avatar': visitor_obj2.avatar,
                    'link': visitor_obj2.link
                }
            })
        list.append({
            'id': message_item_id,
            'message': item.message,
            'time': local_time.strftime('%Y-%m-%d'),
            'visitor': {
                'name': visitor_obj.name,
                'id': visitor_obj.id,
                'avatar': visitor_obj.avatar,
                'link': visitor_obj.link
            },
            'child_message_list': child_list
        })
    data = {
        "code": "200",
        "msg": "成功",
        "data": list
    }
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json", charset='utf-8',
                        status='200', reason='success')

#添加留言
#POST
def addLiveMessage(request):
    try:
        data_string = json.loads(request.body)
        message = data_string['comment']
        user_name = data_string['name']
        localTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        user_obj = Visitor.objects.get(name=user_name)
        replay_id = data_string['replay_id']
    except Exception as e:
        print(e, '获取前端传回的数据失败')
    if replay_id == '':
        message_obj = LiveMessage(message=message, visitor_id=user_obj.id, created_time=localTime)
    else:
        message_obj = LiveMessage(message=message, visitor_id=user_obj.id, created_time=localTime,
                                  parent_comment_id=replay_id)
    message_obj.save()
    data = {
        "code": "200",
        "msg": "成功"
    }
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json", charset='utf-8',
                        status='200', reason='success')

#def getOpenid(request):
#    url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx94864d8a37bde769&redirect_uri=https%3A%2F%2Fapi.' \
#          'brightness.xin%2Fapi%2Fget_wechat_code&response_type=code&scope=snsapi_userinfo&connect_redirect=1#wechat' \
#          '_redirect'
#    img = qrcode.make(url)
#    with open('test.png', 'wb') as f:
#        img.save(f)
#    image_data = open('test.png', "rb").read()
#    data = {
#        "code": "200",
#        "msg": "成功"
#    }
#    return HttpResponse(image_data, content_type="image/png")

#解析微信返回的数据
def process_response_login(rsp):
    try:
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
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=wx94864d8a37bde769&secret=d6b1fa96c1c0b2f931aa5edf' \
          'dec4d793&code=%s&grant_type=authorization_code' % code
    token, err = process_response_login(requests.get(url))
    if not err:
        _access_token = token['access_token']
        _openid = token['openid']
        res_data = {
            '_access_token': _access_token,
            '_openid': _openid
        }
    return res_data

def getWechatCode(request):
    try:
        code = request.GET.get('code')
        res_data = getWxAppid(code)
        openid = res_data['_openid']
        access_token = res_data['_access_token']
    except Exception as e:
        print(e, '获取前端数据失败')

    try:
        url = 'https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s' % (access_token, openid)
        print('url', url)
        token, err = process_response_login(requests.get(url))
        if not err:
            print('subscribe', token['city'])
            print('token', token)
        else:
            print('获取失败', err)
    except Exception as e:
        print(e, '获取用户信息失败')

    data = {
        "code": "200",
        "msg": "成功"
    }

    return HttpResponse(json.dumps(token, ensure_ascii=False), content_type="application/json", charset='utf-8',
                        status='200', reason='success')
