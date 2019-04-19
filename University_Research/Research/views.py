# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect
from django.shortcuts import render
import json
from django.core.files.storage import FileSystemStorage
from django.core.mail import get_connection
from django.core import serializers
from Research.forms import LoginS
from Research.forms import medit
from Research.forms import LoginSu
from Research.forms import LoginD
from Research.forms import viewM
from Research.forms import newMessage
from Research.forms import snewMessage
from Research.models import Comments
from Research.models import Superior
from Research.models import Scholar
from Research.forms import Passed
from Research.models import Subjected
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
levels=[(1,"Zeroth Review"),(2,"First DC"),(3,"Coursework Completion"),(4,"Comprehensive Viva"),(5,"Second DC"),(6,"Third DC"),(7,"Synopsis Submission"),(8,"RASC"),(9,"Thesis Submission"),(10,"Open Defence")]
def home(request):
  if request.session.has_key('mid') or request.session.has_key('regno'):
     logg="Logout"
  else:
     logg="Login"
  return render(request,"home.html",{"logg":logg})

def login(request):
  logg="Login"
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
  elif request.session.has_key('superior'):
    return HttpResponseRedirect('/logoutsp/')
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
  elif request.session.has_key('superior'):
    return HttpResponseRedirect('/superview/')
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
         return render(request,"login.html",{"message":"Password Changed Successfully","col":"green","logg":"Login"})
      else:
         del request.session['regno']
         return render(request,"login.html",{"message":"Incorrect Old Password","col":"red","logg":"Login"})
    else:
      del request.session['regno']
      return render(request,"login.html",{"message":"Incorrect Information!","col":"red","logg":"Login"})
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
       return render(request,"login.html",{"message":"Your account is yet to be approved","col":"orange","logg":"Login"})  
    else:
     return render(request,"login.html",{"message":"Invalid Username or Password","col":"red","logg":"Login"})
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
     return render(request,"login.html",{"message":"Invalid Username or Password","col":"red","logg":"Login"})
  else:
    return render(request,"login.html",{})

def logout(request):
  try:
    del request.session['regno']
    return render(request,"login.html",{"message":"Logged out successfully!","col":"green","logg":"Login"})
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
  return render(request,"login.html",{"message":"Logged out successfully!","col":"green","logg":"Login"})

def logoutsp(request):
  try:
    del request.session['superior']
    if request.session.has_key('stored'):
      del request.session['stored']
  except:
    pass
  return render(request,"login.html",{"message":"Logged out successfully!","col":"green","logg":"Login"})

def loginsu(request):
  if request.POST:
    MyUseForm=LoginSu(request.POST)
    if MyUseForm.is_valid():
      dbN=Supervisor.objects.get(mid=MyUseForm.cleaned_data['mid'])
      if dbN.approved==True:
        request.session['mid']=dbN.mid
        return HttpResponseRedirect('/supervisor1')
      else:
        return render(request,"login.html",{"message":"Your account is yet to be approved","col":"orange","logg":"Login"})
    else:
      return render(request,"login.html",{"message":"Invalid Username or Password","col":"red","logg":"Login"})
  else:
    return render(request,"login.html",{})

def scholar1(request):
  if request.session.has_key('mid') or request.session.has_key('regno'):
     logg="Logout"
  else:
     logg="Login"
  status1=""
  current=""
  unread=0
  rno=request.session['regno']
  dbP=Personal_Det.objects.get(scholar__regno=rno)
  dbPu=Publications.objects.filter(scholars__regno=rno)
  dbUpcoming=Progress.objects.filter(scholar__regno=rno).order_by('level').exclude(result="pass")
  dbNext=""
  dbRest=""
  if dbUpcoming:
    dbNext=dbUpcoming[0]
    dbRest=dbUpcoming[1:]
  dbSubjects=Progress.objects.get(scholar__regno=rno,level=3)
  subjects=dbSubjects.subjected_set.all()
  dbMessages=Message.objects.filter(scholar__regno=rno).order_by('-latest')
  for message in dbMessages:
    if message.schunread==True:
      unread=unread+1
  dbCompleted=Progress.objects.filter(scholar__regno=rno,result="pass").order_by('-level')
  dbLatest=dbCompleted[0]
  dbOthers=dbCompleted[1:]
  dbSu=Su_Personal_Det.objects.get(supervisor__mid=dbP.supervisor.mid)
  reports=""
  DCguys=DCMembers.objects.filter(scholar__regno=rno)
  current=dbCompleted[0].name
  if unread==0:
    unread=""
  return render(request,"scholar1.html",{"name":dbP.name,"current":current,"dob":dbP.dob,"sex":dbP.sex,"reports":reports,"regno":dbP.scholar.regno,"regdate":dbP.regdate,"school":dbP.school,"pubs":dbPu,"supervisor":dbSu.name,"levels":levels,"logg":logg,"dbNext":dbNext,"dbRest":dbRest,"dbLatest":dbLatest,"dbOthers":dbOthers,"dbMessages":dbMessages,"unread":unread,"subjects":subjects})

def supervisor1(request):
  if request.session.has_key('mid') or request.session.has_key('regno'):
     logg="Logout"
  else:
     logg="Login"
  if request.session.has_key('stored'):
     del request.session['stored']
  mid=request.session['mid']
  unread=0
  dbMessages=Message.objects.filter(supervisorText__mid=mid).order_by('-latest')
  for message in dbMessages:
    if message.supunread==True:
      unread=unread+1
  dbP=Su_Personal_Det.objects.get(supervisor__mid=mid)
  dbPu=Publications.objects.filter(supervisors__mid=mid).values()
  dbSch=Personal_Det.objects.filter(supervisor__mid=mid)
  if unread==0:
    unread=""
  return render(request,"supervisor1.html",{"logg":logg,"pubs":dbPu,"sch":dbSch,"name":dbP.name,"email":dbP.email,"sex":dbP.sex,"school":dbP.school,"mid":dbP.supervisor.mid,"aoi":dbP.aoi,"dbMessages":dbMessages,"unread":unread})

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
       return render(request,"suinfo.html",{"pubs":dbPu,"sch":dbSch,"name":dbP.name,"email":dbP.email,"sex":dbP.sex,"school":dbP.school,"mid":dbP.supervisor.mid,"aoi":dbP.aoi,"logg":"Logout"})
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
  elif request.session.has_key('superior'):
    return HttpResponseRedirect('/sprinfo')
  else:
    return HttpResponseRedirect('/profile')
  if request.session.has_key('stored'):
    mdid=request.session['mid']
    dbDean=Supervisor.objects.get(mid=mdid)
    if dbDean.dean:
      rno=request.session['stored']
      dbP=Personal_Det.objects.get(scholar__regno=rno)
      dbUpcoming=Progress.objects.filter(scholar__regno=rno).order_by('level').exclude(result="pass")
      dbNext=""
      dbRest=""
      if dbUpcoming:
        dbNext=dbUpcoming[0]
        dbRest=dbUpcoming[1:]
      dbSubjects=Progress.objects.get(scholar__regno=rno,level=3)
      subjects=dbSubjects.subjected_set.all()
      dbCompleted=Progress.objects.filter(scholar__regno=rno,result="pass").order_by('-level')
      DCguys=DCMembers.objects.filter(scholar__regno=rno)
      return render(request,"dschprog.html",{"logg":logg,"name":dbP.name,"dbCompleted":dbCompleted,"dbNext":dbNext,"dbRest":dbRest,"subjects":subjects})
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
    dbNext=""
    dbRest=""
    if dbUpcoming:
      dbNext=dbUpcoming[0]
      dbRest=dbUpcoming[1:]
    dbSubjects=Progress.objects.get(scholar__regno=rno,level=3)
    subjects=dbSubjects.subjected_set.all()
    today=datetime.datetime.today().strftime('%d-%b-%Y')
    dbCompleted=Progress.objects.filter(scholar__regno=rno,result="pass").order_by('-level')
    DCguys=DCMembers.objects.filter(scholar__regno=rno)
    return render(request,"schprog.html",{"logg":logg,"name":dbP.name,"dbCompleted":dbCompleted,"dbNext":dbNext,"dbRest":dbRest,"today":today,"subjects":subjects})
  else:
    return render(request,"home.html",{})

def bookAppointment(request):
  return render(request,"calendar.html", {} )


def dmake(request):
  if request.POST:
    edited=medit(request.POST)
    if edited.is_valid():
      rno=request.session['stored']
      dlevel=edited.cleaned_data['level']
      move=edited.cleaned_data['move']
      dbC=Progress.objects.get(scholar__regno=rno,level=3)
      courses=dbC.subjected_set.all()
      level=Progress.objects.get(scholar__regno=rno,level=dlevel)
      name=Personal_Det.objects.get(scholar__regno=rno).name
      return render(request,"dschedit.html",{"move":move,"name":name,"level":level,"courses":courses,"logg":"Logout"})
  else:
    return HttpResponseRedirect('/profile')

def makedit(request):
  if request.POST:
    edited=medit(request.POST)
    if edited.is_valid():
      rno=request.session['stored']
      dlevel=edited.cleaned_data['level']
      move=edited.cleaned_data['move']
      dbC=Progress.objects.get(scholar__regno=rno,level=3)
      courses=dbC.subjected_set.all()
      level=Progress.objects.get(scholar__regno=rno,level=dlevel)
      name=Personal_Det.objects.get(scholar__regno=rno).name
      return render(request,"schedit.html",{"move":move,"name":name,"level":level,"courses":courses,"logg":"Logout"})
    else:
      print form.errors
      return HttpResponseRedirect('/profile')
  else:
    return HttpResponseRedirect('/profile')

def schedule(request):
  if request.POST:
    sForm=Schedule(request.POST)
    if sForm.is_valid():
      date=sForm.cleaned_data['date']
      start=sForm.cleaned_data['start']
      end=sForm.cleaned_data['end']
      if request.session.has_key('stored'):
        rno=request.session['stored']
        current=Progress.objects.filter(scholar__regno=rno).order_by('level').exclude(result="pass")[0]
        current.date=date
        current.start=start
        current.end=end
        current.save()
        return HttpResponseRedirect('/dschprog')
    else:
      print form.errors
      return HttpResponseRedirect('/profile')
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
  if request.session.has_key('mid'):
    mmid=request.session['mid']
    dbDean=Supervisor.objects.get(mid=mmid)
    if dbDean:
       dbPersonal=Personal_Det.objects.get(scholar__regno=rno)
       dbProgress=Progress.objects.filter(scholar__regno=rno).order_by('level').exclude(result="pass")[0]
       name=dbPersonal.name
       return render(request,"plusdc.html",{"name":name,"dcLevel":dbProgress,"logg":"Logout"})
  else:
    return HttpResponseRedirect('/profile')

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
    unread=0
    dbD=Supervisor.objects.get(mid=mid,dean=True)
    dbA=Personal_Det.objects.only("name","scholar")
    dbSList=Su_Personal_Det.objects.only("name","supervisor")
    Schcnt=Scholar.objects.filter().count()
    Supcnt=Supervisor.objects.filter().count()-1
    dbMessages=Message.objects.filter(deanText__mid='deanresearch@sastra.edu').order_by('-latest')
    dates=[]
    dbDs=Progress.objects.filter().all()
    for Ds in dbDs:
      dated={}
      if Ds.level == 2:
        if Ds.date:
          dated['title'] = 'First DC for ' + Ds.scholar.personal_det.name
          dated['start'] = str(Ds.date) + "T" + str(Ds.start)
          dated['end'] = str(Ds.date) + "T" + str(Ds.end)
          dates.append(dated)
      elif Ds.level == 5:
        if Ds.date:
          dated['title'] = 'Second DC for ' + Ds.scholar.personal_det.name
          dated['start'] = str(Ds.date) + "T" + str(Ds.start)
          dated['end'] = str(Ds.date) + "T" + str(Ds.end)
          dates.append(dated)
      elif Ds.level == 6:
        if Ds.date:
          dated['title'] = 'Third DC for ' + Ds.scholar.personal_det.name
          dated['start'] = str(Ds.date) + "T" + str(Ds.start)
          dated['end'] = str(Ds.date) + "T" + str(Ds.end)
          dates.append(dated)
    dates=json.dumps(dates)
    for message in dbMessages:
      if message.deanunread:
        unread=unread+1
    if unread==0:
      unread=""
    return render(request,"dean1.html",{"logg":logg,"trig":0,"mid":mid,"sch":Schcnt,"sup":Supcnt,"dbA":dbA,"dbSList":dbSList,"unread":unread,"dbMessages":dbMessages,"dates":dates})

def sureg(request):
  if request.POST:
    RegSu=suregForm(request.POST)
    if RegSu.is_valid():
      if RegSu.cleaned_data['exin']=="Other":
         SuuObj=Supervisor(mid=RegSu.cleaned_data['email'],password=mid)
         SuuObj.save()
         SuObj.institution=RegSu.cleaned_data['institution']
         SuObj.designation=RegSu.cleaned_data['designation']
         SuObj=Su_Personal_Det(name=RegSu.cleaned_data['name'],sex=RegSu.cleaned_data['sex'],school=RegSu.cleaned_data['school'],email=RegSu.cleaned_data['email'],aoi=RegSu.cleaned_data['aoi'],phno=RegSu.cleaned_data['phno'])
         SuObj.supervisor=SuuObj
         SuObj.save()
         SuuObj.save()
         message="Registered Successfully! The Member ID is: "+str(mid)
         head="Approval for Supervisor "+RegSu.cleaned_data['name']
         dObj=Supervisor.objects.get(mid='deanresearch@sastra.edu')
         mObj=Message(head=head,supervisorText=SuuObj,sender='supervisor',deanText=dObj,deanunread=True)
         mObj.save()
         return render(request,"login.html",{"message":message,"logg":"Login"})
      else:
         SuuObj=Supervisor(mid=RegSu.cleaned_data['email'],password=RegSu.cleaned_data['mid'])
         SuuObj.save()
         SuObj=Su_Personal_Det(name=RegSu.cleaned_data['name'],sex=RegSu.cleaned_data['sex'],school=RegSu.cleaned_data['school'],email=RegSu.cleaned_data['email'],aoi=RegSu.cleaned_data['aoi'],phno=RegSu.cleaned_data['phno'],pemail=RegSu.cleaned_data['pemail'])
         SuObj.institution="SASTRA"
         SuObj.designation=""     
         SuObj.supervisor=SuuObj
         SuObj.save()
         SuuObj.save()
         head="Approval for Supervisor "+RegSu.cleaned_data['name']
         dObj=Supervisor.objects.get(mid='deanresearch@sastra.edu')
         mObj=Message(head=head,supervisorText=SuuObj,sender='supervisor',deanText=dObj,deanunread=True)
         mObj.save()
         return render(request,"login.html",{"message":"Registered Successfully!","col":"green","logg":"Login"})
    else:
      return render(request,"login.html",{"message":"Couldn't register!","col":"red","logg":"Login"})
  else:
    return render(request,"home.html",{})

def schreg(request):
  if request.POST:
    RegS=schregForm(request.POST)
    if RegS.is_valid():
      SObj=Personal_Det(name=RegS.cleaned_data['name'],sex=RegS.cleaned_data['sex'],dob=RegS.cleaned_data['dob'],school=RegS.cleaned_data['school'],email=RegS.cleaned_data['email'],regdate=RegS.cleaned_data['regdate'],category=RegS.cleaned_data['category'],phno=RegS.cleaned_data['phno'],retitle=RegS.cleaned_data['retitle'],typet=RegS.cleaned_data['typet'])
      TObj=Scholar(regno=RegS.cleaned_data['email'],password=RegS.cleaned_data['regno'])
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
        elif key == 9:
          thesis=Thesis(level=key,name=values,scholar=TObj,result="yet")
          thesis.save()
      head="Approval for Scholar - "+RegS.cleaned_data['name']
      dObj=Supervisor.objects.get(mid='deanresearch@sastra.edu')
      mObj=Message(head=head,sender='scholar',scholar=TObj,deanText=dObj,deanunread=True)
      mObj.save()
      return render(request,"login.html",{"message":"Registered Successfully!","col":"green","logg":"Login"})
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

def spreg(request):
  return render(request,"sureg.html",{})

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
          dProg.datePaid=date
          dProg.fees="Paid"
          dProg.save()
          return HttpResponseRedirect('/schprog')
    else:
      print form.errors
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
        dbProg.save()
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
  
def newText(request):
  if request.POST:
    mData=newMessage(request.POST)
    if mData.is_valid():
      receiver=mData.cleaned_data['receiver']
      title=mData.cleaned_data['title']
      content=mData.cleaned_data['content']
      rno=request.session['regno']
      sObj=Personal_Det.objects.get(scholar__regno=rno)
      mObj=Message(head=title,body=content,scholar=sObj.scholar,sender=sObj.name)
      if receiver == '1':
        suObj=sObj.supervisor
        mObj.supervisorText=suObj
        mObj.supunread=True
      elif receiver == '2':
        suObj=Supervisor.objects.get(mid='deanresearch@sastra.edu')
        mObj.deanText=suObj
        mObj.deanunread=True
      elif receiver == '3':
        suObj=sObj.supervisor
        suObj1=Supervisor.objects.get(mid='deanresearch@sastra.edu')
        mObj.supervisorText=suObj
        mObj.deanText=suObj1
        mObj.supunread=True
        mObj.deanunread=True
      mObj.save()
      return HttpResponseRedirect('/profile')
    else:
      print form.errors
      return HttpResponseRedirect('/profile')
  else:
    print form.errors
    return HttpResponseRedirect('/profile')

def superText(request):
  if request.POST:
    mData=snewMessage(request.POST)
    if mData.is_valid():
      receiver=mData.cleaned_data['receiver']
      scholar=mData.cleaned_data['scholar']
      sObj=Supervisor.objects.get(mid=request.session['mid'])
      title=mData.cleaned_data['title']
      content=mData.cleaned_data['content']
      mObj=Message(head=title,body=content,supervisorText=sObj)
      mObj.sender=Su_Personal_Det.objects.get(supervisor__mid=request.session['mid']).name
      if receiver == '1':
        rno=scholar.split(' ')[0]
        mObj.scholar=Scholar.objects.get(regno=rno)
        mObj.schunread=True
      elif receiver == '2':
        mObj.deanText=Supervisor.objects.get(mid='deanresearch@sastra.edu')
        mObj.deanunread=True
      else:
        rno=scholar.split(' ')[0]
        mObj.scholar=Scholar.objects.get(regno=rno)
        mObj.deanText=Supervisor.objects.get(mid='deanresearch@sastra.edu')
        mObj.deanunread=True
      mObj.save()
      return HttpResponseRedirect('/profile')
    else:
      print form.errors
      return HttpResponseRedirect('/profile')
  else:
    return HttpResponseRedirect('/profile')
  
def texted(request):
  if request.session.has_key('regno'):
    return render(request,"newText.html",{})
  else:
    return HttpResponseRedirect('/profile')

def stexted(request):
  if request.session.has_key('mid'):
    return render(request,"snewText.html",{})
  else:
    return HttpResponseRedirect('/profile')

def dtexted(request):
  if request.session.has_key('mid'):
    return render(request,"dnewText.html",{})
  else:
    return HttpResponseRedirect('/profile')

def Mview(request):
  if request.POST:
    vData=viewM(request.POST)
    if vData.is_valid():
      tid=vData.cleaned_data['tid']
      request.session['tid']=tid
      return HttpResponseRedirect('/viewText')
    else:
      print form.errors
      return HttpResponseRedirect('/profile')
  else:
    return HttpResponseRedirect('/profile')

def viewText(request):
  if request.session.has_key('tid'):
    tid=request.session['tid']
    tMObj=Message.objects.get(tid=tid)
    if request.session.has_key('regno'):
      if tMObj.schunread==True:
        tMObj.schunread=False
        tMObj.save()
    if request.session.has_key('mid'):
      mmid=Supervisor.objects.get(mid=request.session['mid'])
      if mmid.dean:
        if tMObj.deanunread==True:
          tMObj.deanunread=False
          tMObj.save()
      else:
        if tMObj.supunread==True:
          tMObj.supunread=False
          tMObj.save()
    comments=Comments.objects.filter(message__tid=tid)
    return render(request,"viewText.html",{"tMObj":tMObj,"comments":comments,"logg":"Logout"})

def addComment(request):
  if request.POST:
    cData=commentForm(request.POST)
    if cData.is_valid():
      tid=request.session['tid']
      tObj=Message.objects.get(tid=tid)
      cObj=Comments(message=tObj,content=cData.cleaned_data['content'])
      if request.session.has_key('regno'):
        rno=request.session['regno']
        sObj=Personal_Det.objects.get(scholar__regno=rno)
        cObj.sender=sObj.name
      elif request.session.has_key('mid'):
        mid=request.session['mid']
        mObj=Supervisor.objects.get(mid=mid)
        if mObj.dean:
          cObj.sender="Dean"
        else:
          mdObj=Su_Personal_Det.objects.get(supervisor__mid=mid)
          cObj.sender=mdObj.name
      cObj.save()
      return HttpResponseRedirect('/viewText')
    return HttpResponseRedirect('/profile')
  return HttpResponseRedirect('/profile')

def dcPass(request):
  if request.POST:
    dcObj=request.POST.getlist('course[]')
    hComment=request.POST.get('hComment')
    level=request.POST.get('level')
    rno=request.session['stored']
    dbProg=Progress.objects.get(scholar__regno=rno,level=level)
    dbNext=Progress.objects.get(scholar__regno=rno,level=3)
    dbProg.comments=hComment
    dbProg.result="pass"
    dbProg.save()
    for subj in dcObj:
      nS=Subjected(name=subj,course=dbNext)
      nS.save()
    return HttpResponseRedirect('/schprog')
  else:
    print form.errors
    return HttpResponseRedirect('/profile')

def courseEdit(request):
  if request.POST:
    dcObj=request.POST.getlist('course[]')
    level=request.POST.get('level')
    rno=request.session['stored']
    dbProg=Progress.objects.get(scholar__regno=rno,level=level)
    for subj in dcObj:
      nS=Subjected(name=subj,course=dbProg)
      nS.save()
    return HttpResponseRedirect('/schprog')
  else:
    return HttpResponseRedirect('/profile')

def marked(request):
  if request.POST:
    dcMarks=request.POST.getlist('marks[]')
    dcDate=request.POST.getlist('date[]')
    dcResult=request.POST.getlist('result[]')
    rno=request.session['stored']
    dbProg=Progress.objects.get(scholar__regno=rno,level=3)
    subjects=dbProg.subjected_set.all()
    i=0
    res="pass"
    for subject in subjects:
      subject.marks=dcMarks[i]
      subject.datePassed=dcDate[i]
      subject.status=dcResult
      subject.save()
      if dcResult=="fail":
        res="fail"
      i=i+1
    if res=="pass":
      dbProg.result="pass"
      dbProg.save()
    return HttpResponseRedirect('/schprog')
  else:
    return HttpResponseRedirect('/profile')

def supApprove(request):
  if request.POST:
    tid=request.POST.get('tid')
    mObj=Message.objects.get(tid=tid)
    mid=mObj.supervisorText.mid
    suObj=Su_Personal_Det.objects.get(supervisor__mid=mid)
    return render(request,"supApprove.html",{"mObj":mObj,"suObj":suObj})
  else:
    return HttpResponseRedirect('/profile')

def superApprove(request):
  if request.POST:
    approve=request.POST.get('approval')
    if approve=='approved':
      mid=request.POST.get('mid')
      sObj=Supervisor.objects.get(mid=mid)
      sObj.approved=True
      sObj.save()
      MObj=Message.objects.get(sender='supervisor',supervisorText=sObj)
      MObj.delete()
      return HttpResponseRedirect('/profile')
    else:
      return HttpResponseRedirect('/profile')
  else:
    return HttpResponseRedirect('/profile')

def schApprove(request):
  if request.POST:
    tid=request.POST.get('tid')
    mObj=Message.objects.get(tid=tid)
    regno=mObj.scholar.regno
    name = Personal_Det.objects.get(scholar__regno=regno).name
    return render(request,"schApprove.html",{"name":name,"mObj":mObj})
  else:
    return HttpResponseRedirect('/profile')

def sApprove(request):
  if request.POST:
    approve = request.POST.get('approval')
    date = request.POST.get('date')
    regno = request.POST.get('regno')
    if approve == 'approved':
      sObj=Scholar.objects.get(regno=regno)
      sObj.approved=True
      sObj.save()
      pObj=Progress.objects.get(level=1,scholar__regno=regno)
      pObj.result='pass'
      pObj.presented=date
      pObj.save()
      mObj=Message.objects.get(sender="scholar",scholar=sObj).delete()
      return HttpResponseRedirect('/profile')
    else:
      return HttpResponseRedirect('/profile')
  else:
    return HttpResponseRedirect('/profile')

def deanText(request):
  if request.POST:
    receiver=request.POST.get('receiver')
    if receiver == '1':
      regno = request.POST.get('scholar')
      name = request.POST.get('title')
      content = request.POST.get('content')
      sObj=Scholar.objects.get(regno=regno)
      dObj=Supervisor.objects.get(mid='deanresearch@sastra.edu')
      mObj= Message(head=name,body=content,scholar=sObj,deanText=dObj,sender='Dean',schunread=True)
      mObj.save()
    elif receiver == '2':
      mid = request.POST.get('supervisor')
      name = request.POST.get('title')
      content = request.POST.get('content')
      sObj = Supervisor.objects.get(mid=mid)
      dObj = Supervisor.objects.get(mid='deanresearch@sastra.edu')
      mObj = Message(head=name,body=content,supervisorText=sObj,deanText=dObj,sender='Dean',supunread=True)
      mObj.save()
    elif receiver == '3':
      mid = request.POST.get('supervisor')
      regno = request.POST.get('scholar')
      name = request.POST.get('title')
      content = request.POST.get('content')
      sObj = Scholar.objects.get(regno=regno)
      suObj = Supervisor.objects.get(mid=mid)
      dObj = Supervior.objects.get(mid='deanresearch@sastra.edu')
      mObj = Message(head=name,body=content,scholar=sObj,supervisorText=suObj,deanText=dObj,sender='Dean',schunread=True,supunread=True)
      mObj.save()
    return HttpResponseRedirect('/profile')
  else:
    return HttpResponseRedirect('/profile')

def plusComment(request):
  if request.POST:
    tid=request.POST.get('tid')
    mObj=Message.objects.get(tid=tid)
    content=request.POST.get('newcomment')
    if request.session.has_key('regno'):
      regno=request.session['regno']
      name=Personal_Det.objects.get(scholar__regno=regno).name
      mObj.supunread=True
      mObj.deanunread=True
    elif request.session.has_key('mid'):
      mid=request.session['mid']
      dObj=Supervisor.objects.get(mid=mid)
      if dObj.dean:
        name="Dean"
        mObj.supunread=True
        mObj.schunread=True
      else:
        name=Su_Personal_Det.objects.get(supervisor__mid=mid).name
        mObj.schunread=True
        mObj.deanunread=True
    cObj=Comments(content=content,sender=name,message=mObj)
    cObj.save()
    mObj.latest=datetime.datetime.now()
    mObj.save()
    return HttpResponseRedirect('/viewText')
  else:
    return HttpResponseRedirect('/profile')

def thesis(request):
  if request.POST and request.FILES['thesisdoc']:
    thesisdoc = request.FILES['thesisdoc']
    rno=request.session['regno']
    dbNow=Progress.objects.filter(scholar__regno=rno).exclude(result='pass')[0]
    dbNow.doc=thesisdoc
    dbNow.save()
    return HttpResponseRedirect('/profile')
  return HttpResponseRedirect('/profile')

def synopsis(request):
  if request.POST and request.FILES['syndoc']:
    syndoc = request.FILES['syndoc']
    rno=request.session['regno']
    dbNow=Progress.objects.filter(scholar__regno=rno).exclude(result='pass')[0]
    dbNow.doc=syndoc
    dbNow.save()
    return HttpResponseRedirect('/profile')
  return HttpResponseRedirect('/profile')

def schform(request):
  return render(request,"schreg.html",{})

def addpub(request):
  regno=request.session['stored']
  name=Personal_Det.objects.get(scholar__regno=regno).name
  return render(request,"addpub.html",{"name":name})

def pubPlus(request):
  regno=request.session['stored']
  mid=request.session['mid']
  sObj=Scholar.objects.get(regno=regno)
  suObj=Supervisor.objects.get(mid=mid)
  dbP=Publications(title=request.POST['title'],name=request.POST['name'],date=request.POST['year'])
  dbP.save()
  dbP.scholars.add(sObj)
  dbP.supervisors.add(suObj)
  dbP.save()
  return HttpResponseRedirect('/profile')

def schpub(request):
  regno=request.session['stored']
  name=Personal_Det.objects.get(scholar__regno=regno).name
  pubs=Publications.objects.filter(scholars__regno=regno)
  return render(request,"schpub.html",{"pubs":pubs,"name":name})

def dschpub(request):
  regno=request.session['stored']
  name=Personal_Det.objects.get(scholar__regno=regno).name
  pubs=Publications.objects.filter(scholars__regno=regno)
  return render(request,"dschpub.html",{"pubs":pubs,"name":name})

def loginm(request):
  if request.POST:
    MyUseForm=LoginS(request.POST)
    if MyUseForm.is_valid():
     dbN=Scholar.objects.filter(regno=MyUseForm.cleaned_data['regno'])
     if dbN:
       dbN=Scholar.objects.get(regno=MyUseForm.cleaned_data['regno'])
       if dbN.approved==True:
         request.session['regno']=dbN.regno
         request.session['regno']=MyUseForm.cleaned_data['regno']
         return HttpResponseRedirect('/scholar1')
       else:
         return render(request,"login.html",{"message":"Your account is yet to be approved","col":"orange","logg":"Login"})
     dbN=Supervisor.objects.filter(mid=MyUseForm.cleaned_data['regno'])
     if dbN:
       dbN=Supervisor.objects.get(mid=MyUseForm.cleaned_data['regno'])
       if dbN.approved==False:
         return render(request,"login.html",{"message":"Your account is yet to be approved","col":"orange","logg":"Login"})
       isLoggedIn = True #change to false for shanmail-auth
       connection=get_connection(host='mail.sastra.edu',port=587,username=MyUseForm.cleaned_data['regno'],password=MyUseForm.cleaned_data['password'],use_tls=False)
       try:
         connection.open()
       except:
         isLoggedIn=True
       else:
         isLoggedIn=True
       if dbN and isLoggedIn:
         request.session['mid']=MyUseForm.cleaned_data['regno']
         if dbN.dean:
           return HttpResponseRedirect('/dean1')
         else:
           return HttpResponseRedirect('/supervisor1')
       else:
         return render(request,"login.html",{"message":"Invalid Username or Password","col":"red","logg":"Login"})
     else:
       dbN=Superior.objects.filter(email=MyUseForm.cleaned_data['regno'])
       if dbN:
         isLoggedIn = True
         connection=get_connection(host='mail.sastra.edu',port=587,username=MyUseForm.cleaned_data['regno'],password=MyUseForm.cleaned_data['password'],use_tls=False)
         try:
           connection.open()
         except:
           pass
         else:
           isLoggedIn=True
         if dbN and isLoggedIn:
           request.session['superior']=MyUseForm.cleaned_data['regno']
           return HttpResponseRedirect('/superview')
         else:
           return render(request,"login.html",{"message":"Invalid Username or Password","col":"red","logg":"Login"})
       else:
         return render(request,"login.html",{"message":"Invalid Username or Password","col":"red","logg":"Login"})
    else:
       return render(request,"login.html",{"message":"Invalid Username or Password","col":"red","logg":"Login"})
  else:
    return render(request,"login.html",{})

def viewer(request):
  if request.POST:
    IForm=infof(request.POST)
    if IForm.is_valid():
      rdata=IForm.cleaned_data['regno']
      rno=rdata.split()[0]
      request.session['stored']=rno
      return HttpResponseRedirect('/sprinfo')
    else:
      return HttpResponseRedirect('/profile')
  else:
    return HttpResponseRedirect('/profile')

def superview(request):
  if request.session.has_key('superior'):
      logg="Logout"
  else:
      return HttpResponseRedirect('/login/')
  dbA=Personal_Det.objects.only("name","scholar")
  dbSList=Su_Personal_Det.objects.only("name","supervisor")
  return render(request,"superview.html",{"dbA":dbA,"dbSList":dbSList,"logg":logg})


def sprinfo(request):
  if request.session.has_key('superior'):
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
    return render(request,"sprinfo.html",{"logg":logg,"name":dbP.name,"dob":dbP.dob,"sex":dbP.sex,"email":dbP.email,"regno":dbP.scholar.regno,"regdate":dbP.regdate,"school":dbP.school,"pubs":dbPu,"supervisor":dbSu.name,"status1":current})
  else:
    return render(request,"home.html",{})

def spschprog(request):
  if request.session.has_key('superior'):
    logg="Logout"
  else:
    return HttpResponseRedirect('/profile')
  if request.session.has_key('stored'):
    current=""
    rno=request.session['stored']
    dbP=Personal_Det.objects.get(scholar__regno=rno)
    dbUpcoming=Progress.objects.filter(scholar__regno=rno).order_by('level').exclude(result="pass")
    dbNext=""
    dbRest=""
    if dbUpcoming:
      dbNext=dbUpcoming[0]
      dbRest=dbUpcoming[1:]
    dbSubjects=Progress.objects.get(scholar__regno=rno,level=3)
    subjects=dbSubjects.subjected_set.all()
    today=datetime.datetime.today().strftime('%d-%b-%Y')
    dbCompleted=Progress.objects.filter(scholar__regno=rno,result="pass").order_by('-level')
    DCguys=DCMembers.objects.filter(scholar__regno=rno)
    return render(request,"spschprog.html",{"logg":logg,"name":dbP.name,"dbCompleted":dbCompleted,"dbNext":dbNext,"dbRest":dbRest,"today":today,"subjects":subjects})
  else:
    return render(request,"home.html",{})

def noThird(request):
  if request.session.has_key('mid'):
    regno=request.session['stored']
    dbThird=Progress.objects.get(scholar__regno=regno,level=6)
    dbThird.result="pass"
    dbThird.current=True
    dbThird.save()
    return HttpResponseRedirect('/schprog')
  else:
    return HttpResponseRedirect('/profile')