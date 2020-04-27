from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

#禁止CSRF校验
@csrf_exempt
def myPost(request):
    #从HTTP POST中请求user字段值
    user = str(request.POST.get('user'))
    #从HTTP POST请求中获取age字段值
    age = str(request.POST.get('age'))

    result = '<h2>name:<font color="red">' + user + '</font></h2>'
    result += '<h2>age:<font color="blue">' + age + '</font></h2>'

    return HttpResponse(result)