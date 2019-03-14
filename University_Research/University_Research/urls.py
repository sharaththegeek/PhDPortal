"""University_Research URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from Research.views import home 
from django.views.generic import TemplateView
from Research.views import logins
from Research.views import ann
from Research.views import login1
from Research.views import login
from Research.views import loginsu
from Research.views import logind
from Research.views import schprog
from Research.views import superm
from Research.views import super1
from Research.views import super2
from Research.views import super3
from Research.views import super4
from Research.views import support
from Research.views import scholar1
from Research.views import dean1
from Research.views import schedit
from Research.views import schstart
from Research.views import schinfo
from Research.views import suinfo
from Research.views import supervisor1
from Research.views import adett
from Research.views import reg
from Research.views import schreg
from Research.views import chnpwd
from Research.views import newann
from Research.views import dschinfo
from Research.views import sureg
from Research.views import adup
from Research.views import profile
from Research.views import annd
from Research.views import logout
from Research.views import logq
from Research.views import supmes
from Research.views import readj
from Research.views import storesch
from Research.views import logoutsu

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^readj/', readj),
    url(r'^home/', home),
    url(r'^logq/', logq),
    url(r'^login/',login),
    url(r'^schprog/',schprog),
    url(r'^storesch/',storesch),
    url(r'^login1/',login1),
    url(r'^chnpwd/',chnpwd),
    url(r'^login1/',login1),
    url(r'^ann/',ann),
    url(r'^logind/',logind),
    url(r'^logins/',logins),
    url(r'^loginsu/',loginsu),
    url(r'^annd/',annd),
    url(r'^superm/',superm),
    url(r'^super1/',super1),
    url(r'^super2/',super2),
    url(r'^newann/',newann),
    url(r'^suinfo/',suinfo),
    url(r'^logout/',logout),
    url(r'^profile/',profile),
    url(r'^logoutsu/',logoutsu),
    url(r'^super3/',super3),
    url(r'^super4/',super4),
    url(r'^scholar1/',scholar1),
    url(r'^dean1/',dean1),
    url(r'^support/',support),
    url(r'^supervisor1',supervisor1),
    url(r'^schedit',schedit),
    url(r'^schstart',schstart),
    url(r'^schinfo',schinfo),
    url(r'^dschinfo',dschinfo),
    url(r'^reg',reg),
    url(r'^adett',adett),
    url(r'^schreg',schreg),
    url(r'^adup',adup),
    url(r'^sureg',sureg),
    url(r'^supmes',supmes),
]
