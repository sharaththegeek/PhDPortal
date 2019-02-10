from django import forms
from Research.models import Scholar
from Research.models import Supervisor
from django.core.validators import MaxValueValidator, MinValueValidator
class LoginS(forms.Form):
  regno=forms.CharField(max_length=17)
  password=forms.CharField(widget=forms.PasswordInput())

  def clean_regno(self):
      regno=self.cleaned_data.get("regno")
      dbn=Scholar.objects.filter(regno=regno)
      if not dbn:
        raise forms.ValidationError("Incorrect Username")
      else:
        return regno
  
  def clean_password(self):
      regno=self.cleaned_data.get("regno")
      password=self.cleaned_data.get("password")
      dbn=Scholar.objects.filter(regno=regno)
      if not dbn:
       raise forms.ValidationError("Incorrect Username")
      else:
       dbm=Scholar.objects.get(regno=regno)
       dbp1=dbm.password
       dbp=(password==dbp1)
       if not dbp:
         raise forms.ValidationError("Incorrect Password")
       else:
         return password

class LoginSu(forms.Form):
  mid=forms.CharField(max_length=15)
  password=forms.CharField(widget=forms.PasswordInput())

  def clean_mid(self):
      mid=self.cleaned_data.get("mid")
      dbn=Supervisor.objects.filter(mid=mid)
      if not dbn:
        raise forms.ValidationError("Incorrect Username")
      else:
        return mid

  def clean_password(self):
      mid=self.cleaned_data.get("mid")
      password=self.cleaned_data.get("password")
      dbn=Supervisor.objects.filter(mid=mid)
      if not dbn:
       raise forms.ValidationError("Incorrect Username")
      else:
       dbm=Supervisor.objects.get(mid=mid)
       dbd=dbm.dean
       if dbd:
         raise forms.ValidationError("Not Eligible")
       else:
        dbp1=dbm.password
        dbp=(password==dbp1)
        if not dbp:
          raise forms.ValidationError("Incorrect Password")
        else:
          return password

class LoginD(forms.Form):
  mid=forms.CharField(max_length=15)
  password=forms.CharField(widget=forms.PasswordInput())

  def clean_mid(self):
      mid=self.cleaned_data.get("mid")
      dbn=Supervisor.objects.filter(mid=mid)
      if not dbn:
        raise forms.ValidationError("Incorrect Username")
      else:
        return mid

  def clean_password(self):
      mid=self.cleaned_data.get("mid")
      password=self.cleaned_data.get("password")
      dbn=Supervisor.objects.filter(mid=mid)
      if not dbn:
       raise forms.ValidationError("Incorrect Username")
      else:
       dbm=Supervisor.objects.get(mid=mid)
       dbp1=dbm.password
       dbd=dbm.dean
       if not dbd:
         raise forms.ValidationError("Not Eligible")
       else:
        dbp=(password==dbp1)
        if not dbp:
          raise forms.ValidationError("Incorrect Password")
        else:
          return password

class PwdForm(forms.Form):
  old=forms.CharField(widget=forms.PasswordInput())
  new=forms.CharField(widget=forms.PasswordInput())
  newd=forms.CharField(widget=forms.PasswordInput())
  
  def clean_newd(self):
    new=self.cleaned_data.get("new")
    newd=self.cleaned_data.get("newd")
    if new==newd:
      return newd
    else:
      raise forms.ValidationError("Incorrect")

class editform(forms.Form):
  status=forms.CharField(max_length=10)
  date=forms.DateField()
  remarks=forms.CharField(max_length=500)
  progress=forms.CharField(max_length=30)
  regno=forms.CharField(max_length=17)

class infof(forms.Form):
  regno=forms.CharField(max_length=17)

class startform(forms.Form):
  date=forms.DateField()
  message=forms.CharField(max_length=500)
  progress=forms.CharField(max_length=30)
  regno=forms.CharField(max_length=17)

class regnosearchForm(forms.Form):
  regno=forms.CharField(max_length=17)
 
class namesearchForm(forms.Form):
  regno=forms.CharField(max_length=30)
  
class SunamesearchForm(forms.Form):
  mid=forms.CharField(max_length=30)

class midsearchForm(forms.Form):
  mid=forms.CharField(max_length=15)

class suregForm(forms.Form):
   name=forms.CharField(max_length=30)
   lname=forms.CharField(max_length=30)
   sex=forms.CharField(max_length=10)
   phno=forms.CharField(max_length=11)
   mid=forms.CharField(max_length=15)
   school=forms.CharField(max_length=30)
   email=forms.EmailField()
   pemail=forms.EmailField()
   aoi=forms.CharField(max_length=500)
   exin=forms.CharField(max_length=30)
   institution=forms.CharField(max_length=500)
   designation=forms.CharField(max_length=300)

class schregForm(forms.Form):
   name=forms.CharField(max_length=30)
   lname=forms.CharField(max_length=30)
   sex=forms.CharField(max_length=10)
   dob=forms.DateField()
   category=forms.CharField(max_length=10)
   regno=forms.CharField(max_length=17)
   school=forms.CharField(max_length=30)
   email=forms.EmailField()
   pemail=forms.EmailField()
   phno=forms.CharField(max_length=11)
   supervisor=forms.CharField(max_length=15)
   regdate=forms.DateField()
   retitle=forms.CharField(max_length=500)
   typet=forms.CharField(max_length=30)
   exin=forms.CharField(max_length=30)
   institution=forms.CharField(max_length=500)
   institution_ad=forms.CharField(max_length=500)

class AnForm(forms.Form):
   title=forms.CharField(max_length=200)
   body=forms.CharField(max_length=1000)
   
   
class dcmForm(forms.Form):
   mmid=forms.CharField(max_length=15)
   regno=forms.CharField(max_length=17)

class repupForm(forms.Form):
   head=forms.CharField(max_length=100)
   body=forms.CharField(max_length=1000)
   regno=forms.CharField(max_length=17)

class supForm(forms.Form):
   desig=forms.CharField(max_length=30)
   head=forms.CharField(max_length=100)
   body=forms.CharField(max_length=1000)
