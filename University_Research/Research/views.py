# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect
from django.shortcuts import render
import json
from django.core import serializers
from Research.forms import LoginS
from Research.forms import medit
from Research.forms import LoginSu
from Research.forms import LoginD
from Research.models import Scholar
from Research.forms import Passed
from Research.forms import NextPass
from Research.models import Personal_Det
from Research.forms import oEdit
from Research.models import Su_Personal_Det
from Research.models import Supervisor
from Research.models import Publications
from Research.models import DCMembers
from Research.models import Progress
from Research.forms import hForm
from Research.forms import Schedule
from Research.forms import dcComment
from Research.forms import ZerothF
from Research.models import DC
from Research.models import Coursework
from Research.models import Others
from Research.models import Thesis
from Research.models import Zero
from Research.forms import editform
from Research.forms import regnosearchForm
from Research.forms import startform
from Research.models import Message
from Research.forms import infof
from Research.serializers import AnnouncementSerializer
import datetime
from rest_framework.renderers import JSONRenderer
from Research.forms import namesearchForm
from Research.forms import dcmForm
from Research.models import Announcement
from Research.forms import SunamesearchForm
from Research.forms import midsearchForm
from Research.forms import schregForm
from Research.forms import suregForm
from Research.forms import AnForm
from Research.models import SupMess
from Research.forms import supForm
from Research.forms import repupForm
from Research.forms import PwdForm
import random
# Create your views here.
logg="Login"
levels=[(1,"Zeroth Review"),(2,"First DC"),(3,"Coursework Completion"),(4,"Comprehensive Viva"),(5,"Second DC"),(6,"Third DC"),(7,"Synopsis Submission"),(8,"RAC"),(9,"Thesis Submission"),(10,"Open Defence")]
def home(request):
  if request.session.has_key('mid') or request.session.has_key('regno'):
     logg="Logout"
  else:
     logg="Login"
  return render(request,"home.html",{"logg":logg})

def login(request):
  if request.session.has_key('mid') or request.session.has_key('regno'):
     logg="Logout"
  else:
     logg="Login"
  return render(request,"login.html",{"logg":logg})

def newann(request):
  if request.POST:
    AnnF=AnForm(request.POST)
    if AnnF.is_valid():
      da=datetime.datetime.now()
      NAn=Announcement(title=AnnF.cleaned_data['title'],body=AnnF.cleaned_data['body'],adate=da)
      NAn.save()
      return HttpResponseRedirect('/annd')
    else:
      return render(request,"home.html",{})
  else:
    return render(request,"home.html",{})

def readj(request):
  dbAAA=Announcement.objects.all()
  dbAA=Personal_Det.objects.all()
  dbA=serializers.serialize('json',dbAA,fields=("name","scholar"))
  return render(request,"index.html",{"dbA":dbA,"dbAA":dbAA})
  
def annd(request):
  if request.session.has_key('mid'):
    dbA=Announcement.objects.filter()
    return render(request,"annd.html",{"dbA":dbA})
  else: 
    return HttpResponseRedirect('/login1')

def logq(request):
  if request.session.has_key('mid'): 
    return HttpResponseRedirect('/logoutsu/')    
  elif request.session.has_key('regno'):
    return HttpResponseRedirect('/logout/')
  else:
    return HttpResponseRedirect('/login/')

def profile(request):
  if request.session.has_key('mid'):
    mid=request.session['mid']
    dbS=Supervisor.objects.get(mid=mid)
    if dbS.dean:
       return HttpResponseRedirect('/dean1/')
    else:
       return HttpResponseRedirect('/supervisor1/')
  elif request.session.has_key('regno'):
    return HttpResponseRedirect('/scholar1/')
  else:
    return HttpResponseRedirect('/login1/')

def ann(request):
  if request.session.has_key('mid') or request.session.has_key('regno'):
    dbA=Announcement.objects.all()
    dbCount=Announcement.objects.filter().count()
    noOfPages=dbCount/10
    return render(request,"ann.html",{"dbA":dbA,"dbCount":dbCount,"noOfPages":noOfPages})
  else:
    return HttpResponseRedirect('/login1')

def adett(request):
  if request.POST:
    dcmm=dcmForm(request.POST)
    if dcmm.is_valid():
      mi=dcmm.cleaned_data['mmid']
      regno=dcmm.cleaned_data['regno']
      dbSS=Su_Personal_Det.objects.filter(supervisor__mid=mi).values()
      if dbSS.exists():
        dbSSS=Supervisor.objects.get(mid=mi)
        dbD=DC_Meeting.objects.get(scholar__regno=regno,progress="B")
        dbD.supervisors.add(dbSSS)
        dbD.save()
        return HttpResponseRedirect('/profile/')
      else:
        return render(request,"home.html",{})
    else:
      return render(request,"home.html",{})
  else:
    return render(request,"home.html",{})


def chnpwd(request):
  if request.POST:
    PwdF=PwdForm(request.POST)
    if PwdF.is_valid():
      regno=request.session['regno']
      dbS=Scholar.objects.get(regno=regno)
      pd=dbS.password
      if PwdF.cleaned_data['old']==pd:
         dbS.password=PwdF.cleaned_data['new']
         dbS.save()
         del request.session['regno']
         return render(request,"login.html",{"message":"Password Changed Successfully","col":"green"})
      else:
         del request.session['regno']
         return render(request,"login.html",{"message":"Incorrect Old Password","col":"red"})
    else:
      del request.session['regno']
      return render(request,"login.html",{"message":"Incorrect Information!","col":"red"})
  else:
     return render(request,"home.html",{})


def logins(request):
  if request.POST:
    MyUseForm=LoginS(request.POST)
    if MyUseForm.is_valid():
     dbN=Scholar.objects.get(regno=MyUseForm.cleaned_data['regno'])
     if dbN.approved==True:
       request.session['regno']=dbN.regno
       return HttpResponseRedirect('/scholar1')
     else:
       return render(request,"login.html",{"message":"Your account is yet to be approved","col":"orange"})  
    else:
     return render(request,"login.html",{"message":"Invalid Username or Password","col":"red"})
  else:
    return render(request,"login.html",{})

def logind(request):
  if request.POST:
    MyUseForm=LoginD(request.POST)
    if MyUseForm.is_valid():
     dbN=Supervisor.objects.get(mid=MyUseForm.cleaned_data['mid'])
     request.session['mid']=dbN.mid
     return HttpResponseRedirect('/dean1')
    else:
     return render(request,"login.html",{"message":"Invalid Username or Password","col":"red"})
  else:
    return render(request,"login.html",{})

def logout(request):
  try:
    del request.session['regno']
    return render(request,"login.html",{"message":"Logged out successfully!","col":"green"})
  except:
    pass
    return render(request,"login.html",{})

def logoutsu(request):
  try:
    del request.session['mid']
    if request.session.has_key('stored'):
      del request.session['stored']
  except:
    pass
  return render(request,"login.html",{"message":"Logged out successfully!","col":"green"})

def loginsu(request):
  if request.POST:
    MyUseForm=LoginSu(request.POST)
    if MyUseForm.is_valid():
      dbN=Supervisor.objects.get(mid=MyUseForm.cleaned_data['mid'])
      if dbN.approved==True:
        request.session['mid']=dbN.mid
        return HttpResponseRedirect('/supervisor1')
      else:
        return render(request,"login.html",{"message":"Your account is yet to be approved","col":"orange"})
    else:
      return render(request,"login.html",{"message":"Invalid Username or Password","col":"red"})
  else:
    return render(request,"login.html",{})

def scholar1(request):
  if request.session.has_key('mid') or request.session.has_key('regno'):
     logg="Logout"
  else:
     logg="Login"
  status1=""
  current=""
  rno=request.session['regno']
  dbP=Personal_Det.objects.get(scholar__regno=rno)
  dbPu=Publications.objects.filter(scholars__regno=rno)
  dbUpcoming=Progress.objects.filter(scholar__regno=rno).order_by('level').exclude(result="pass")
  dbNext=dbUpcoming[0]
  dbRest=dbUpcoming[1:]
  dbMessages=Message.objects.filter(scholar__regno=rno)
  dbCompleted=Progress.objects.filter(scholar__regno=rno,result="pass").order_by('-level')
  dbLatest=dbCompleted[0]
  dbOthers=dbCompleted[1:]
  dbSu=Su_Personal_Det.objects.get(supervisor__mid=dbP.supervisor.mid)
  reports=""
  DCguys=DCMembers.objects.filter(scholar__regno=rno)
  current=dbCompleted[0].name
  return render(request,"scholar1.html",{"name":dbP.name,"current":current,"dob":dbP.dob,"sex":dbP.sex,"reports":reports,"regno":dbP.scholar.regno,"regdate":dbP.regdate,"school":dbP.school,"pubs":dbPu,"supervisor":dbSu.name,"status1":status1,"levels":levels,"logg":logg,"dbNext":dbNext,"dbRest":dbRest,"dbLatest":dbLatest,"dbOthers":dbOthers,"dbMessage":dbMessage})

def supervisor1(request):
  if request.session.has_key('mid') or request.session.has_key('regno'):
     logg="Logout"
  else:
     logg="Login"
  if request.session.has_key('stored'):
     del request.session['stored']
  mid=request.session['mid']
  dbP=Su_Personal_Det.objects.get(supervisor__mid=mid)
  dbPu=Publications.objects.filter(supervisors__mid=mid).values()
  dbSch=Personal_Det.objects.filter(supervisor__mid=mid)
  return render(request,"supervisor1.html",{"logg":logg,"pubs":dbPu,"sch":dbSch,"name":dbP.name,"email":dbP.email,"sex":dbP.sex,"school":dbP.school,"mid":dbP.supervisor.mid,"aoi":dbP.aoi})

def suinfo(request):
  if request.POST:
     SuF=midsearchForm(request.POST)
     if SuF.is_valid():
       formdata=SuF.cleaned_data['mid']
       spos=formdata.find(' ')
       mid=formdata[:spos]
       dbP=Su_Personal_Det.objects.get(supervisor__mid=mid)
       dbPu=Publications.objects.filter(supervisors__mid=mid).values()
       dbSch=Personal_Det.objects.filter(supervisor__mid=mid)
       return render(request,"suinfo.html",{"pubs":dbPu,"sch":dbSch,"name":dbP.name,"email":dbP.email,"sex":dbP.sex,"school":dbP.school,"mid":dbP.supervisor.mid,"aoi":dbP.aoi})
  else:
     return render(request,"home.html",{})

def dschinfo(request):
  if request.session.has_key('mid'):
    logg="Logout"
  else:
    return HttpResponseRedirect('/profile')
  status1=""
  if request.session.has_key('stored'):
    mdid=request.session['mid']
    dbDean=Supervisor.objects.get(mid=mdid)
    if dbDean.dean:
      rno=request.session['stored']
      dbP=Personal_Det.objects.get(scholar__regno=rno)
      dbPu=Publications.objects.filter(scholars__regno=rno)
      dbSu=Su_Personal_Det.objects.get(supervisor__mid=dbP.supervisor.mid)
      dbCompleted=Progress.objects.filter(scholar__regno=rno,result="pass").order_by('-level')
      current=dbCompleted[0].name
      return render(request,"dschinfo.html",{"logg":logg,"name":dbP.name,"dob":dbP.dob,"sex":dbP.sex,"email":dbP.email,"regno":dbP.scholar.regno,"regdate":dbP.regdate,"school":dbP.school,"pubs":dbPu,"supervisor":dbSu.name,"status1":current})
    else:
      return render(request,"home.html",{})
  else:
    return render(request,"home.html",{})

def dschprog(request):
  if request.session.has_key('mid'):
    logg="Logout"
  else:
    return HttpResponseRedirect('/profile')
  if request.session.has_key('stored'):
    mdid=request.session['mid']
    dbDean=Supervisor.objects.get(mid=mdid)
    if dbDean.dean:
      rno=request.session['stored']
      dbP=Personal_Det.objects.get(scholar__regno=rno)
      dbUpcoming=Progress.objects.filter(scholar__regno=rno).order_by('level').exclude(result="pass")
      dbNext=dbUpcoming[0]
      dbRest=dbUpcoming[1:]
      dbCompleted=Progress.objects.filter(scholar__regno=rno,result="pass").order_by('-level')
      DCguys=DCMembers.objects.filter(scholar__regno=rno)
      return render(request,"dschprog.html",{"logg":logg,"name":dbP.name,"dbCompleted":dbCompleted,"dbNext":dbNext,"dbRest":dbRest})
    else:
      return HttpResponseRedirect('/profile')
  else:
    return render(request,"home.html",{})

def storesch(request):
  if request.POST:
    IForm=infof(request.POST)
    if IForm.is_valid():
      mdid=request.session['mid']
      dbDean=Supervisor.objects.get(mid=mdid)
      if dbDean.dean:
        rdata=IForm.cleaned_data['regno']
        rno=rdata.split()[0]
        request.session['stored']=rno
        return HttpResponseRedirect('/dschinfo')
      else: 
        rno=IForm.cleaned_data['regno']
        request.session['stored']=rno
        return HttpResponseRedirect('/schinfo')
  else:
    return render(request,"home.html",{})

def schinfo(request):
  if request.session.has_key('mid'):
    logg="Logout"
  else:
    return HttpResponseRedirect('/profile')
  status1=""
  if request.session.has_key('stored'):
    rno=request.session['stored']
    dbP=Personal_Det.objects.get(scholar__regno=rno)
    dbPu=Publications.objects.filter(scholars__regno=rno)
    dbSu=Su_Personal_Det.objects.get(supervisor__mid=dbP.supervisor.mid)
    dbCompleted=Progress.objects.filter(scholar__regno=rno,result="pass").order_by('-level')
    current=dbCompleted[0].name
    return render(request,"schinfo.html",{"logg":logg,"name":dbP.name,"dob":dbP.dob,"sex":dbP.sex,"email":dbP.email,"regno":dbP.scholar.regno,"regdate":dbP.regdate,"school":dbP.school,"pubs":dbPu,"supervisor":dbSu.name,"status1":current})
  else:
    return render(request,"home.html",{})

def schprog(request):
  if request.session.has_key('mid'):
    logg="Logout"
  else:
    return HttpResponseRedirect('/profile')
  if request.session.has_key('stored'):
    current=""
    rno=request.session['stored']
    dbP=Personal_Det.objects.get(scholar__regno=rno)
    dbUpcoming=Progress.objects.filter(scholar__regno=rno).order_by('level').exclude(result="pass")
    dbNext=dbUpcoming[0]
    dbRest=dbUpcoming[1:]
    today=datetime.datetime.today().strftime('%d-%b-%Y')
    dbCompleted=Progress.objects.filter(scholar__regno=rno,result="pass").order_by('-level')
    DCguys=DCMembers.objects.filter(scholar__regno=rno)
    return render(request,"schprog.html",{"logg":logg,"name":dbP.name,"dbCompleted":dbCompleted,"dbNext":dbNext,"dbRest":dbRest,"today":today})
  else:
    return render(request,"home.html",{})

def dmake(request):
  if request.POST:
    edited=medit(request.POST)
    if edited.is_valid():
      rno=request.session['stored']
      dlevel=edited.cleaned_data['level']
      move=edited.cleaned_data['move']
      level=Progress.objects.get(scholar__regno=rno,level=dlevel)
      name=Personal_Det.objects.get(scholar__regno=rno).name
      return render(request,"dschedit.html",{"move":move,"name":name,"level":level})
  else:
    return HttpResponseRedirect('/profile')

def makedit(request):
  if request.POST:
    edited=medit(request.POST)
    if edited.is_valid():
      rno=request.session['stored']
      dlevel=edited.cleaned_data['level']
      move=edited.cleaned_data['move']
      level=Progress.objects.get(scholar__regno=rno,level=dlevel)
      name=Personal_Det.objects.get(scholar__regno=rno).name
      return render(request,"schedit.html",{"move":move,"name":name,"level":level})
  else:
    return HttpResponseRedirect('/profile')

def schedule(request):
  if request.POST:
    sForm=Schedule(request.POST)
    if sForm.is_valid():
      date=sForm.cleaned_data['date']
      time=sForm.cleaned_data['time']
      if request.session.has_key('stored'):
        rno=request.session['stored']
        current=Progress.objects.filter(scholar__regno=rno).order_by('level').exclude(result="pass")[0]
        current.date=date
        current.time=time
        current.save()
        return HttpResponseRedirect('/schprog')
  else:
    return HttpResponseRedirect('/profile')

def dsched(request):
  if request.POST:
    IForm=infof(request.POST)
    if IForm.is_valid():
      rdata=IForm.cleaned_data['regno']
      rno=rdata.split()[0]
      request.session['stored']=rno
      mdid=request.session['mid']
      dbDean=Supervisor.objects.get(mid=mdid)
      if dbDean.dean:
        return HttpResponseRedirect('/plusdc')
      else: 
        return HttpResponseRedirect('/schinfo')
  else:
    return render(request,"home.html",{})

def plusdc(request):
  if request.session.has_key('mid'):
    logg="Logout"
  else:
    return HttpResponseRedirect('/profile')
  if request.session.has_key('stored'):
    rno=request.session['stored']
  else:
    return HttpResponseRedirect('/profile')
  dbPersonal=Personal_Det.objects.get(scholar__regno=rno)
  dbProgress=Progress.objects.filter(scholar__regno=rno).order_by('level').exclude(result="pass")[0]
  name=dbPersonal.name
  return render(request,"plusdc.html",{"name":name,"dcLevel":dbProgress})

def schstart(request):
  if request.POST:
    SForm=startform(request.POST)
    if SForm.is_valid():
      dbS=DC_Meeting.objects.get(scholar__regno=SForm.cleaned_data['regno'],progress=SForm.cleaned_data['progress'])
      dbS.sdate=SForm.cleaned_data['date']
      dbS.message=SForm.cleaned_data['message']
      dbS.Started=True
      dbS.save()
      return HttpResponseRedirect('/supervisor1')
    else:
      return render(request,"login.html",{})
  else:
    return render(request,"home.html",{})

def dean1(request):
    if request.session.has_key('mid') or request.session.has_key('regno'):
      logg="Logout"
    else:
      logg="Login"
    mid=request.session['mid']
    dbD=Supervisor.objects.get(mid=mid,dean=True)
    dbA=Personal_Det.objects.only("name","scholar")
    dbSList=Su_Personal_Det.objects.only("name","supervisor")
    Schcnt=Scholar.objects.filter().count()
    Supcnt=Supervisor.objects.filter().count()-1
    now=datetime.datetime.now()
    supmessage=SupMess.objects.filter(mid=0).values()
    supmessage1=SupMess.objects.filter(regno=0).values()
    if now.hour<12:
      message="Good Morning..."
    elif now.hour>=12 and now.hour<16:
      message="Good Afternoon..."
    else:
      message="Good Evening..."
    return render(request,"dean1.html",{"logg":logg,"trig":0,"message":message,"mid":mid,"sch":Schcnt,"sup":Supcnt,"supmessage":supmessage,"supmessage1":supmessage1,"dbA":dbA,"dbSList":dbSList})

def sureg(request):
  if request.POST:
    RegSu=suregForm(request.POST)
    if RegSu.is_valid():
      if RegSu.cleaned_data['exin']=="Other":
         check=True
         mid=0
         while(check):
           mid=random.randint(200000000,200009999)
           dbC=Supervisor.objects.filter(mid=mid)
           if not dbC.exists():
             check=False
         SuuObj=Supervisor(mid=mid,password=mid)
         SuuObj.save()
         SuObj.institution=RegSu.cleaned_data['institution']
         SuObj.designation=RegSu.cleaned_data['designation']
         SuObj=Su_Personal_Det(name=RegSu.cleaned_data['name'],sex=RegSu.cleaned_data['sex'],school=RegSu.cleaned_data['school'],email=RegSu.cleaned_data['email'],aoi=RegSu.cleaned_data['aoi'],phno=RegSu.cleaned_data['phno'],pemail=RegSu.cleaned_data['pemail'])
         SuObj.supervisor=SuuObj
         SuObj.save()
         SuuObj.save()
         message="Registered Successfully! The Member ID is: "+str(mid)
         return render(request,"login.html",{"message":message})
      else:
         SuuObj=Supervisor(mid=RegSu.cleaned_data['mid'],password=RegSu.cleaned_data['mid'])
         SuuObj.save()
         SuObj=Su_Personal_Det(name=RegSu.cleaned_data['name'],sex=RegSu.cleaned_data['sex'],school=RegSu.cleaned_data['school'],email=RegSu.cleaned_data['email'],aoi=RegSu.cleaned_data['aoi'],phno=RegSu.cleaned_data['phno'],pemail=RegSu.cleaned_data['pemail'])
         SuObj.institution="SASTRA"
         SuObj.designation=""     
         SuObj.supervisor=SuuObj
         SuObj.save()
         SuuObj.save()
         return render(request,"login.html",{"message":"Registered Successfully!","col":"green"})
    else:
      return render(request,"login.html",{"message":"Couldn't register!","col":"red"})
  else:
    return render(request,"home.html",{})

def schreg(request):
  if request.POST:
    RegS=schregForm(request.POST)
    if RegS.is_valid():
      SObj=Personal_Det(name=RegS.cleaned_data['name'],sex=RegS.cleaned_data['sex'],dob=RegS.cleaned_data['dob'],school=RegS.cleaned_data['school'],email=RegS.cleaned_data['email'],regdate=RegS.cleaned_data['regdate'],category=RegS.cleaned_data['category'],pemail=RegS.cleaned_data['pemail'],phno=RegS.cleaned_data['phno'],retitle=RegS.cleaned_data['retitle'],typet=RegS.cleaned_data['typet'])
      TObj=Scholar(regno=RegS.cleaned_data['regno'],password=RegS.cleaned_data['regno'])
      SuObj=Supervisor.objects.get(mid=RegS.cleaned_data['supervisor'])
      SObj.supervisor=SuObj
      TObj.save()
      if RegS.cleaned_data['exin']=="Other":
        SObj.institution=RegS.cleaned_data['institution']
        SObj.institution_ad=RegS.cleaned_data['institution_ad']
      else:
        SObj.institution="SASTRA"
        SObj.institution_ad=""
      SObj.scholar=TObj
      SObj.save()
      SuObj.save()
      TObj.save()
      for key,values in levels:
        if key == 1:
          zer=Zero(level=key,name=values,scholar=TObj,result="yet")
          zer.save()
        elif key == 2 or key == 5 or key == 6:
          dcd=DC(level=key,name=values,scholar=TObj,result="yet")
          dcd.save()
        elif key == 3:
          cor=Coursework(level=key,name=values,scholar=TObj,result="yet")
          cor.save()
        elif key == 4 or key == 7 or key == 8 or key == 10:
          other=Others(level=key,name=values,scholar=TObj,result="yet")
          other.save()
        elif key == 10:
          thesis=Thesis(level=key,name=values,scholar=TObj,result="yet")
          thesis.save()
      return render(request,"login.html",{"message":"Registered Successfully!","col":"green"})
    else:
      errmess=schregForm.errors
      errmess1=schregForm.non_field_errors
      return render(request,"login.html",{"message":errmess,"col":"red"})
  else:
    return render(request,"home.html",{})

def adup(request):
   return render(reqeust,"home.html",{})

def login1(request):
  if request.session.has_key('mid') or request.session.has_key('regno'):
     logg="Logout"
  else:
     logg="Login"
  return render(request,"login1.html",{"logg":logg})

def reg(request):
  return render(request,"reg.html",{})

def superm(request):
   return render(request,"super.html",{})

def super1(request):
   return render(request,"super1.html",{})

def super2(request):
   return render(request,"super2.html",{})

def super3(request):
   return render(request,"super3.html",{})

def super4(request):
   return render(request,"super4.html",{})

def support(request):
   if request.session.has_key('mid'):
     logg="Logout"
     midv=request.session['mid']
     desig=midv
     supsch='supervisor'
     return render(request,"support.html",{"logg":logg,"desig":desig,"supsch":supsch})
   elif request.session.has_key('regno'):
     logg="Logout"
     schv=request.session['regno']
     desig=schv
     supsch='scholar'
     return render(request,"support.html",{"logg":logg,"desig":desig,"supsch":supsch})
   else:
     return HttpResponseRedirect('/home')
   

def supmes(request):
  if request.session.has_key('mid') or request.session.has_key('regno'):
    if request.POST:
     Spup=supForm(request.POST)
     if Spup.is_valid():
       if Spup.cleaned_data['desig']=='scholar':
         regno=request.session['regno']
         mid=0
       else: 
         mid=request.session['mid']
         regno=0
       Sobj=SupMess(head=Spup.cleaned_data['head'],body=Spup.cleaned_data['body'],regno=regno,mid=mid)
       Sobj.save()
       return HttpResponseRedirect('/profile')
     else:
       return HttpResponseRedirect('/support')
    else:
     return HttpResponseRedirect('/support')
  else:
    return HttpResponseRedirect('/login1')


def zeroth(request):
  if request.POST:
    zero=ZerothF(request.POST)
    if zero.is_valid():
      fee=zero.cleaned_data['fees']
      if fee == "Yes":
        date=zero.cleaned_data['date']
        if request.session.has_key('stored'):
          rno=request.session['stored']
          dProg=Progress.objects.get(scholar__regno=rno,level=1)
          dProg.date=date
          dProg.fees="Paid"
          dProg.save()
          return HttpResponseRedirect('/schprog')
    else:
      return HttpResponseRedirect('/profile')

def dcComments(request):
  if request.POST:
    cData=dcComment(request.POST)
    if cData.is_valid():
      comments=cData.cleaned_data['comments']
      if request.session.has_key('stored'):
        rno=request.session['stored']
        level=request.session['level']
        dProg=Progress.objects.get(scholar__regno=rno,level=level)
        dProg.comments=comments
        dProg.save()
        return HttpResponseRedirect('/schprog')
    else:
      return HttpResponseRedirect('/profile')
  else:
      return HttpResponseRedirect('/profile')
  
def fail(request):
  if request.POST:
    cData=hForm(request.POST)
    if cData.is_valid():
      date=cData.cleaned_data['date']
      level=cData.cleaned_data['level']
      hComment=cData.cleaned_data['hComment']
      if request.session.has_key('stored'):
        rno=request.session['stored']
        dbProg=Progress.objects.get(scholar__regno=rno,level=level)
        dbProg.date=date
        dbProg.comments=hComment
        dbProg.save()
        return HttpResponseRedirect('/schprog')
    else:
      return HttpResponseRedirect('/profile')

def passed(request):
  if request.POST:
    pData=Passed(request.POST)
    if pData.is_valid():
      hComment=pData.cleaned_data['hComment']
      level=pData.cleaned_data['level']
      if request.session.has_key('stored'):
        rno=request.session['stored']
        dbProg=Progress.objects.get(scholar__regno=rno,level=level)
        dbProg.comments=hComment
        dbProg.result="pass"
        dbProg.save()
        return HttpResponseRedirect('/schprog')
    else:
      return HttpResponseRedirect('/profile')
  else:
    return HttpResponseRedirect('/profile')

def nextPass(request):
  if request.POST:
    pData=NextPass(request.POST)
    if pData.is_valid():
      hComment=pData.cleaned_data['hComment']
      level=pData.cleaned_data['level']
      date=pData.cleaned_data['date']
      if request.session.has_key('stored'):
        rno=request.session['stored']
        dbProg=Progress.objects.get(scholar__regno=rno,level=level)
        dbNext=Progress.objects.get(scholar__regno=rno,level=level+1)
        dbProg.comments=hComment
        dbProg.result="pass"
        dbProg.save()
        dbNext.date=date
        dbNext.save()
        return HttpResponseRedirect('/schprog')
    else:
      return HttpResponseRedirect('/profile')
  else:
    return HttpResponseRedirect('/profile')

def otherEdit(request):
  if request.POST:
    oData=oEdit(request.POST)
    if oData.is_valid():
      date=oData.cleaned_data['date']
      level=oData.cleaned_data['level']
      if request.session.has_key('stored'):
        rno=request.session['stored']
        dbProg=Progress.objects.get(scholar__regno=rno,level=level)
        dbProg.date=date
        return HttpResponseRedirect('/schprog')
    else:
      return HttpResponseRedirect('/profile')
  else:
    return HttpResponseRedirect('/profile')
  
def dcFail(request):
  if request.POST:
    dData=Passed(request.POST)
    if dData.is_valid():
      comment=dData.cleaned_data['hComment']
      level=dData.cleaned_data['level']
      if request.session.has_key('stored'):
        rno=request.session['stored']
        dbProg=Progress.objects.get(scholar__regno=rno,level=level)
        dbProg.comment=comment
        dbProg.save()
        return HttpResponseRedirect('/schprog')
    else:
      return HttpResponseRedirect('/profile')
  else:
    return HttpResponseRedirect('/profile')