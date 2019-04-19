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
from django.conf.urls.static import static
from django.conf import settings
from Research.views import synopsis
from Research.views import superText
from Research.views import pubPlus
from Research.views import loginm
from Research.views import logoutsp
from Research.views import sprinfo
from Research.views import noThird
from Research.views import addpub
from django.contrib import admin
from Research.views import home 
from Research.views import dsched
from Research.views import schform
from django.views.generic import TemplateView
from Research.views import logins
from Research.views import spreg
from Research.views import nextPass
from Research.views import superview
from Research.views import viewer
from Research.views import spschprog
from Research.views import schedule
from Research.views import schpub
from Research.views import dschpub
from Research.views import stexted
from Research.views import thesis
from Research.views import ann
from Research.views import courseEdit
from Research.views import login1
from Research.views import plusdc
from Research.views import schApprove
from Research.views import sApprove
from Research.views import marked
from Research.views import login
from Research.views import loginsu
from Research.views import logind
from Research.views import otherEdit
from Research.views import texted
from Research.views import schprog
from Research.views import newText
from Research.views import superm
from Research.views import super1
from Research.views import super2
from Research.views import super3
from Research.views import super4
from Research.views import support
from Research.views import deanText
from Research.views import dtexted
from Research.views import scholar1
from Research.views import dean1
from Research.views import dcPass
from Research.views import schstart
from Research.views import schinfo
from Research.views import suinfo
from Research.views import supervisor1
from Research.views import adett
from Research.views import reg
from Research.views import zeroth
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
from Research.views import dschprog
from Research.views import superApprove
from Research.views import dmake
from Research.views import supmes
from Research.views import makedit
from Research.views import readj
from Research.views import dcFail
from Research.views import passed
from Research.views import fail
from Research.views import plusComment
from Research.views import Mview
from Research.views import storesch
from Research.views import supApprove
from Research.views import logoutsu
from Research.views import viewText
from Research.views import bookAppointment

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^readj/', readj),
    url(r'^home/', home),
    url(r'^logq/', logq),
    url(r'^viewText/',viewText),
    url(r'^login/',login),
    url(r'^schprog/',schprog),
    url(r'^dschprog/',dschprog),
    url(r'^Mview/',Mview),
    url(r'^storesch/',storesch),
    url(r'^schedule/',schedule),
    url(r'^login1/',login1),
    url(r'^chnpwd/',chnpwd),
    url(r'^login1/',login1),
    url(r'^pubPlus/',pubPlus),
    url(r'^pluspub/',addpub),
    url(r'^supApprove/',supApprove),
    url(r'^otherEdit/',otherEdit),
    url(r'^superApprove/',superApprove),
    url(r'^ann/',ann),
    url(r'^dsched',dsched),
    url(r'^makedit',makedit),
    url(r'^nextPass/',nextPass),
    url(r'^plusComment/',plusComment),
    url(r'^logind/',logind),
    url(r'^logins/',logins),
    url(r'^synopsis/',synopsis),
    url(r'^loginsu/',loginsu),
    url(r'^annd/',annd),
    url(r'^zeroth/',zeroth),
    url(r'^dmake/',dmake),
    url(r'^superm/',superm),
    url(r'^super1/',super1),
    url(r'^super2/',super2),
    url(r'^dcFail/',dcFail),
    url(r'^passed/',passed),
    url(r'^marked/',marked),
    url(r'^fail/',fail),
    url(r'^deanText/',deanText),
    url(r'^newText/',newText),
    url(r'^schpub/',schpub),
    url(r'^dschpub/',dschpub),
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
    url(r'^schstart',schstart),
    url(r'^schinfo',schinfo),
    url(r'^dschinfo',dschinfo),
    url(r'^reg',reg),
    url(r'^plusdc',plusdc),
    url(r'^adett',adett),
    url(r'^schApprove/',schApprove),
    url(r'^sApprove/',sApprove),
    url(r'^dcPass/',dcPass),
    url(r'^schreg/',schreg),
    url(r'^dtexted/',dtexted),
    url(r'^texted/',texted),
    url(r'^stexted/',stexted),
    url(r'^adup',adup),
    url(r'^courseEdit/',courseEdit),
    url(r'^sureg',sureg),
    url(r'^spreg',spreg),
    url(r'^logoutsp',logoutsp),
    url(r'^supmes',supmes),
    url(r'^schform/',schform),
    url(r'^superText/',superText),
    url(r'^thesis',thesis),
    url(r'^loginm/',loginm),
    url(r'^superview/',superview),
    url(r'^sprinfo/',sprinfo),
    url(r'^viewer/',viewer),
    url(r'^calendar/',bookAppointment),
    url(r'^spschprog/',spschprog),
    url(r'^noThird/',noThird),
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)