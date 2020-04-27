from django.http import HttpResponse
import datetime

def myResponse(request):
    return HttpResponse('<h1>hello world!</h1>', content_type='text/html')

#该函数用于向客户端写入Cookie
#如下是函数的definition
#def set_cookie(self, key, value='', max_age=None, expires=None, path='/',
#domain=None, secure=False, httponly=False, samesite=None)

def writeCookie(request):
    #Cookie的到期时间是当前时刻加二十秒
    dt = datetime.datetime.now() + datetime.timedelta(seconds=int(20))
    response = HttpResponse('writeCookie')

    #设置第一个Cookie并通过expires参数设置其有效期
    response.set_cookie('name', 'KLGR', max_age=3)
    #设置第二个Cookie
    response.set_cookie('age', 18)
    return response

def readCookie(request):
    result = ''
    name = str(request.COOKIES.get('name'))
    age = str(request.COOKIES.get('age'))

    result = '<h2>name:<font color="red">' + name + '</font></h2>'
    result += '<h2>age:<font color="blue">' + age + '</font></h2>'
    return HttpResponse(result, content_type='text/html')