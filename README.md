# ToUseDjango
This is my first try of using &amp; learning Django

## 零、What is Django
成熟而全面的Python Web框架，采用MVC设计模式。

## 一、Django工程基础知识
 ### 1.项目文件配置
 一共5个脚本文件。
 - manage.py 命令行工具
 - __init__.py 空脚本文件，代表为一个包
 - settings.py 项目配置文件
 - urls.py URL声明（网站目录）
 - wsgi.py 与WSGI兼容的WEB服务器的入口接口
 
 ### 2.添加路由
 Django需要使用路由将URL与服务端要执行的代码关联。
 Django可以将一个普通的函数变成路由函数，使用正则表达式定义路由。
 
 _新建First.py_
  ```
  from django.http import HttpResponse
  def hello(request):
      return HttpResponse('Hello World!')
  ```
 _替换urls.py中的内容_
  ```
from django.conf.urls import url
from . import First
urlpatterns = [
    url(r'^$', First.hello)
]

  ```
  urlpatterns列表：定义当前工程的所有路由匹配模式。
  列表元素是django.resolvers.RegexURLPatterns类的实例（也是url函数的返回值）。
  url函数的参数：
  - 1.匹配url路径的正则表达式
  - 2.路由函数
  本例只是匹配了根路径。

  _First.py_
  ```
  from django.http import HttpResponse
def hello(request):
    return HttpResponse('Hello World!')

def your(request):
    return HttpResponse('your')

def product(request):
    return HttpResponse('product')

def country(request):
    return HttpResponse('country')
  ```
  _urls.py_
  ```
  from django.conf.urls import url
from . import First

urlpatterns = [
    url(r'^$', First.hello),
    url(r'^your$', First.your),
    url(r'^product\d+$', First.product),
    url(r'^country/China|America$', First.country)
]
  ```
 还可以通过Edit Configurations选择IP和端口号。
 
 ### 3.处理http请求
 客户端访问WEB应用，先得获取用户提交的信息。
 
 HTTP请求数据 = HTTP请求头 + BODY（数据）。
 
 HTTP请求头 = HTTP请求字段 + HTTP GET字段。
 
 BODY数据（包括HTTP POST类型）。
 
 ##### 怎么获取HTTP请求的数据以及HTTP GET字段的值？
 
 每一个路由函数，都有request参数，该参数用来获取HTTP请求的所有数据，它是一个django.cre.handlers.wsgi.WSGIRequest对象。
 对象有一些属性，用来获取一些信息，很常用。
 
 - scheme 获取url的协议头（HTTP HTTPS ……）
 - path 获取url的路径
 - method 获取提交的方法（GET POST）
 - GET 再里面的GET属性可获取HTTP请求的GET值，是一个字典
 - POST 同理
 _例子：request.GET['name']可以获得GET值中名字为name的字段值，name就相当于key_
 
 - META 获取HTTP的请求头字段的值 
 _例子：request.META['REMOTE_ADDR']可以获得客户端的IP地址_
 
 
HTTP请求字段名|含义
-----|-----
CONTENT_LENGTH|请求正文的长度
CONTENT_TYPE|请求正文的MIME类型
HTTP_ACCEPT|可接收的CONTENT TYPE
HTTP_ACCEPT_ENCODING|响应可接收的编码
HTTP_ACCEPT_LANGUAGE|可接收的语言
HTTP_HOST|客户端发送的HTTP HOST头
HTTP_REFERER|Referring页面
HTTP_USER_AGENT|用户代理（user-agent字符串）
QUERY_STRING|字符串形式的查询字符串（还没解析的）
REMOTE_ADDR|客户端的IP地址
REMOTE_HOST|客户端的主机名
REMOTE_USER|服务器认证的用户
REQUEST_METHOD|HTTP请求方法（GET POST）
SERVER_NAME|服务器主机名
SERVER_PORT|服务器端口号


代码实例感受一下。

_First.py_
```
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
    # 注意：如果使用GET['GET字段值']获取value 则如果没有该值会报错
    # 然而使用get()方法 在没有值的时候就会返回NULL 不报错 对比一下
    response += 'age:' + str(request.GET.get('age')) + '<br>'
    return HttpResponse(response)
```

_urls.py_
```
from django.conf.urls import url
from . import First

urlpatterns = [
    url('^request$', First.myRequest)
]
```

然后可以比如说尝试一下 http://127.0.0.1:8000/request?name=KLGR

### 4.学习Response和Cookie

现在到最后一步，也就是向客户端返回数据。
如果客户端是浏览器，那么返回HTML,JS,CSS等比较常见。

##### 那么服务端怎么向客户端返回数据？

刚才我们在First.py里多次写入路由函数，且返回值一直是HttpResponse类的实例。
这个类的构造方法可以传入参数request（之前一直是这样，request就等于所要返回的字符串），或者通过content_type关键字参数
指定返回数据的类型（text/html……）。

HttpResponse类中有一个set_cookie方法，作用是用于向客户端写入Cookie数据。
Cookie的本质是通过HTTP响应头的Set-Cookie字段设置的，所以这个方法其实是设置了一下HTTP响应头的该字段值。 

若想要读取Cookie的值，可以用路由函数的request参数。

读取名字为'x'的cookie值的方法：
```
request.COOKIES.get('name')
```

_代码实例，通过WriteCookie函数写入两个Cookie字段值，并通过readCookie函数读取，最后返回给客户端。_
_在本例中还设置了一个Cookie值的过期时间。_

_responseCookie.py_
```
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
    response.set_cookie('name', 'KLGR', expires=dt)
    #设置第二个Cookie
    response.set_cookie('age', 19)
    return response

def readCookie(request):
    result = ''
    name = str(request.COOKIES.get('name'))
    age = str(request.COOKIES.get('age'))

    result = '<h2>name:<font color="red">' + name + '</font></h2>'
    result += '<h2>age:<font color="blue">' + age + '</font></h2>'
    return HttpResponse(result, content_type='text/html')
```

_urls.py_
```
from django.conf.urls import url
from . import responseCookie
from . import First

urlpatterns = [
    url('^request$', First.myRequest),
    #新增
    url(r'^response$', responseCookie.myResponse),
    url(r'^writeCookie$', responseCookie.writeCookie),
    url(r'^readCookie$', responseCookie.readCookie)
]
```

启动服务后，分别输入地址http://localhost:8000/writeCookie 和 http://localhost:8000/writeCookie 查看效果。
如果没有设置Cookie的有效期，则关页面前恒有效；如果设置了则超过时间后无效。

### 5.读写Session

Session类似Cookie，都是通过字典管理键值对。

但是Cookie保存在客户端，Session保存在服务端，这是区别所在。Session在服务端有多种存在方式，一般存储在内存，一旦WEB服务
重启则内存中的Session消失。所以如果想要保存Session使得重启服务器后仍存在，则需要保存到文件或数据库。

Session的一个重要作用就是跟踪客户端，即知道客户端的再次访问的存在。每一个客户端都有单独对用的Session，同时为这个Session创建
一个ID，称之为Session-ID，该Session-ID会利用Cookie的方式保存在客户端。
如果客户端再次访问WEB服务，这个Session-ID也会随着HTTP请求（中的Cookie）发送给WEB服务，WEB服务就会通过这个Session-ID寻找
属于该客户端的Session。

这也意味着如果客户端没有Cookie支持，就无法跟踪之。

读写Session都需要使用路由函数和request参数，WSGIRequest对象有一个Session属性，类型为字典，
故可以通过操作字典的方式读写Session中的键值对。

_session.py_
```
from django.http import HttpResponse
def writeSession(request):
    request.session['name'] = 'klgr'
    request.session['age'] = '22'
    return HttpResponse('writeSession')

def readSession(request):
    result = ''
    name = request.session.get('name')
    age = request.session.get('age')
    if name:
        result = '<h2>name:<font color="red">' + name + '</font></h2>'
    if age:
        result += '<h2>age:<font color="blue">' + str(age) + '</font></h2>'

    return HttpResponse(result, content_type='text/html')
```

_urls.py_
```
from django.conf.urls import url
from . import responseCookie
from . import First
from . import session

urlpatterns = [
    url('^request$', First.myRequest),
    url(r'^response$', responseCookie.myResponse),
    url(r'^writeCookie$', responseCookie.writeCookie),
    url(r'^readCookie$', responseCookie.readCookie),
    url(r'^writeSession$', session.writeSession),
    url(r'^readSession$', session.readSession)
]
```

如果想要改变Session的有效期则要去settings.py修改脚本文件中的SESSION_COOKIE_AGE，以秒计算。

### 6.用户登陆实现

利用Session实现用户登陆的例子。

实现原理：当用户登录成功后，会将用户名和其他信息写入Session。如果用户再次用同一个浏览器访问WEB应用，
就会从客户端对应的Session中重新获取用户名和信息，这样一来第二次访问时，除非Session过期，不然无需登录。

_user.py_
```
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
```

_urls.py_
```
from django.conf.urls import url
from . import responseCookie
from . import First
from . import session
from . import user

urlpatterns = [
    url('^request$', First.myRequest),
    url(r'^response$', responseCookie.myResponse),
    url(r'^writeCookie$', responseCookie.writeCookie),
    url(r'^readCookie$', responseCookie.readCookie),
    url(r'^writeSession$', session.writeSession),
    url(r'^readSession$', session.readSession),
    url(r'^$', user.index),
    url(r'^login$', user.login),
    url(r'^logout$', user.logout)
]
```

之后这么玩：
- 输入http://127.0.0.1:8000/login?user=klgr
- 然后再输入http://127.0.0.1:8000 会显示登陆用户名。
- 访问http://127.0.0.1:8000/logout 注销用户状态。


### 7.静态文件配置

Django的默认静态文件路径是static，在根目录下创建。同时需要修改settings.py脚本文件的INSTALLED_APPS添加当前App的包名，
即根目录的包名。

在该文件夹内放入文件。
然后在地址栏输入http://127.0.0.1:8000/static/文件名 即可访问到文件。

如下代码作为测试。

 - 在static页面创建一个form.html静态页面
 - <form>标签用来提交表单，向服务端提交POST请求
 - 创建post.py脚本文件并添加路由方法处理HTTP POST请求，并返回字段值
 
 _post.py_
 ```
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
 ```

_urls.py_
```
from django.conf.urls import url
from . import responseCookie
from . import First
from . import session
from . import user
from . import post

urlpatterns = [
    url('^request$', First.myRequest),
    url(r'^response$', responseCookie.myResponse),
    url(r'^writeCookie$', responseCookie.writeCookie),
    url(r'^readCookie$', responseCookie.readCookie),
    url(r'^writeSession$', session.writeSession),
    url(r'^readSession$', session.readSession),
    url(r'^$', user.index),
    url(r'^login$', user.login),
    url(r'^logout$', user.logout),
    url(r'^post$', post.myPost)
]
```

_form.html_
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Form</title>
</head>
<body>
    <!-- method绑定post路由函数以自动返回处理后的页面-->
    <form action="/post" method="post">
        User:<input name="user"/><br>
        Age:<input name="age"/><br>
        <input type="submit" value="提交">
    </form>
</body>
</html>
```

先访问form.html并输入以更新request，
然后/post路径通过路由函数处理请求自动返回页面。



## 二、Django模板的使用

### 0.why?

返回数据如果是大的html页面会使得脚本文件臃肿不堪。
Django封装的功能支持很多，这就是Django模板。

### 1.原理简述

Django模板就是HTML静态页面和 _标签_ 的组合。
HTML页面是静态的， _标签_ 是动态的。

由于Django模板文件是通过路由函数返回给客户端的，所以在返回之前， _模板引擎_ 会先将模板
中的所有 _标签_ 替换为静态HTML代码。

只有WEB服务端才能看到这些 _标签_ 并替换之。可以联想微信JS里面的 _变量数据绑定_ 。

所有的 _标签_ 都用{{…}} 括起来，一般内部是一个标识符（变量）。

返回Django模板文件需要使用django.shortcuts模块的render函数。

该函数指定三个参数：
- request:客户端请求
- Django模板文件名
- 字典类型的参数：存储 _标签_ 要替换的值（键值对 key就是标识符）

#### django模板文件默认放置在templates目录下。

首先编写一个hello.html文件并放在static下。

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>hello</title>
</head>
<body>
    <h1>{{ hello }}</h1>
</body>
</html>
```

再建立一个view.py文件，编写路由函数用于返回hello.html文件。

```
from django.shortcuts import render
def hello(request):
    values = {'hello': 'Hello World!'}
    return render(request, 'hello.html', values)
```

_urls.py_

```
from django.conf.urls import url
from . import responseCookie
from . import First
from . import session
from . import user
from . import post
from . import view

urlpatterns = [
    url('^request$', First.myRequest),
    url(r'^response$', responseCookie.myResponse),
    url(r'^writeCookie$', responseCookie.writeCookie),
    url(r'^readCookie$', responseCookie.readCookie),
    url(r'^writeSession$', session.writeSession),
    url(r'^readSession$', session.readSession),
    url(r'^$', user.index),
    url(r'^login$', user.login),
    url(r'^logout$', user.logout),
    url(r'^post$', post.myPost),
    url(r'^hello$', view.hello)
]
```

可以看到，HTML中的变量已经被在路由函数中被替换为指定内容。

### 2.条件控制标签

- {% if condition1 %}
- {% elif condition2 %}
- {% else %}
- {% endif %}

其中必须有的是1和4。

下面是例子。在templates目录中创建一个condition.html文件，其中利用条件控制标签。
然后编写condition.py脚本文件并编写路由函数返回HTML文件，详见代码。

_condition.html_


```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>条件控制</title>
</head>
<body>
{% if condition1 %}
<h1>条件1</h1>
{% elif condition2 %}
<h1>条件2</h1>
{% else %}
<h1>其他条件</h1>
{% endif %}
</body>
</html>
```

_condition.py_

```
from django.shortcuts import render

def myCondition(request):
    values = {'condition1': True, 'condition2': False}
    return render(request, 'condition.html', values)
```

urls.py同理不再赘述。

代码跑起来应该输出“条件1”。

### 3.循环控制标签

- {% for value in value_list %}
-     {{value}}
- {% endfor %}

老规矩，for.html和iteration.py作为测试，见代码。

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>循环控制</title>
</head>
<body>
<ul>
    <!-- values是一个列表变量 -->
    {% for value in value_list %}
        <!-- li标签用作输出列表 -->
        <li>{{value.name}}</li>
    {% endfor %}
</ul>
</body>
</html>
```

```
from django.shortcuts import render

class MyClass:
    name = 'klgr'

def myFor(request):
    #values既包含了字典类型值，也包含对象，只要有名字为name的属性即可
    #使得for.html中与之对应
    Values = {'values': [{'name': 'KLGR'}, MyClass(), {'name': 'klgr'}]}
    return render(request, 'for.html', Values)
```

别忘记配置urls.py。


### 4.过滤器

字母的大小写转换（甚至选定指定字母），日期转换，获取字符串的长度…… _过滤器_ 能帮你。

语法格式：过滤器要放在标签的标识符后面，中间用（|）分隔。

_例子：{{name|upper}}可以将name中的所有英文字母转换为大写。_

filter.html

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>过滤器</title>
</head>
<body>
    {{ value1|upper }}
    <br>
    {{ value2|first|lower }}
    <br>
    {{ value3|length }}
</body>
</html>
```

filter.py

```
from django.shortcuts import render
def myFilter(request):
    values = {}
    values['value1'] = 'hello'
    values['value2'] = 'WORLD'
    values['value3'] = 'how long is this'
    return render(request, 'filter.html', values)
```

urls.py配置。





