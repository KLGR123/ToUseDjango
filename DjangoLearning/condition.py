from django.shortcuts import render

def myCondition(request):
    values = {'condition1': True, 'condition2': False}
    return render(request, 'condition.html', values)