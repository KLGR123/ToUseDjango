from django.http import HttpResponse

def index(request):
    #从Session获取用户名
    user = request.session.get('user')
    result = ''

    #如果成功获取用户名，则表明用户处于登陆状态
    if user:
        result = 'user: %s' % user
    else:
        result = 'Not LOGGED IN'
    return HttpResponse(result)

def login(request):
    #从HTTP GET请求中获取
    user = request.GET.get('user')
    result = ''
    if user:
        request.session['user'] = user
        result = 'login successfully!'
    else:
        result = 'login failed!'
    return HttpResponse(result)

#用于注销登陆的路由
def logout(request):
    try:
        #删除Session中的用户名
        del request.session['user']
    except KeyError:
        pass
    return HttpResponse('You re logged out')