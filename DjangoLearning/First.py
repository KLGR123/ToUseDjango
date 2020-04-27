from django.http import HttpResponse

#路由函数
def myRequest(request):
    response = 'scheme:' + request.scheme + '<br>'
    response += 'path:' + request.path + '<br>'
    response += 'method:' + request.method + '<br>'
    #获取HTTP请求头的信息（利用META属性对应的字段名）
    response += 'HTTP_ACCEPT:' + request.META['HTTP_ACCEPT'] + '<br>'
    response += 'HTTP_USER_AGENT:' + request.META['HTTP_USER_AGENT'] + '<br>'
    response += 'REMOTE_ADDR:' + request.META['REMOTE_ADDR'] + '<br>'
    response += 'QUERY_STRING:' + request.META['QUERY_STRING'] + '<br>'
    #获取name字段的值
    response += 'name:' + str(request.GET['name']) + '<br>'
    # 获取age字段的值
    response += 'age:' + str(request.GET.get('age')) + '<br>'
    return HttpResponse(response)