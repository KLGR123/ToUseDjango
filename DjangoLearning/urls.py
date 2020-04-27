from django.conf.urls import url
from . import responseCookie
from . import First
from . import session
from . import user
from . import post
from . import view
from . import condition
from . import iteration
from . import filter

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
    url(r'^hello$', view.hello),
    url(r'^condition$', condition.myCondition),
    url(r'^for$', iteration.myFor),
    url(r'^filter$', filter.myFilter)
]
