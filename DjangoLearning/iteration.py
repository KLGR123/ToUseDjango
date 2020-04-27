from django.shortcuts import render

class MyClass:
    name = 'klgr'

def myFor(request):
    #values既包含了字典类型值，也包含对象，只要有名字为name的属性即可
    #使得for.html中与之对应
    Values = {'values': [{'name': 'KLGR'}, MyClass(), {'name': 'klgr'}]}
    return render(request, 'for.html', Values)
