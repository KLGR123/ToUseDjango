from django.shortcuts import render
def hello(request):
    values = {'hello': 'Hello World!'}
    return render(request, 'hello.html', values)
