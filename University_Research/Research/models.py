# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from polymorphic.models import PolymorphicModel
from datetime import datetime
# Create your models here.
class Scholar(models.Model):
   regno=models.CharField(max_length=17,primary_key=True)
   password=models.CharField(max_length=30)
   approved=models.BooleanField(default=False)

class Supervisor(models.Model):
   mid=models.CharField(max_length=15,primary_key=True)
   password=models.CharField(max_length=30)
   dean=models.BooleanField(default=False)
   external=models.BooleanField(default=False)
   approved=models.BooleanField(default=False)

class Personal_Det(models.Model):
   name=models.CharField(max_length=50)
   scholar=models.OneToOneField(Scholar)
   email=models.EmailField()
   pemail=models.EmailField()
   category=models.CharField(max_length=10)
   school=models.CharField(max_length=30)
   phno=models.CharField(max_length=11)
   retitle=models.CharField(max_length=500)
   typet=models.CharField(max_length=30)
   regdate=models.CharField(max_length=10)
   sex=models.CharField(max_length=10)
   dob=models.CharField(max_length=10)
   supervisor=models.ForeignKey(Supervisor)
   institution=models.CharField(max_length=500)
   institution_ad=models.CharField(max_length=500)

class Su_Personal_Det(models.Model):
   supervisor=models.OneToOneField(Supervisor)
   name=models.CharField(max_length=50)
   phno=models.PositiveIntegerField()
   email=models.EmailField()
   pemail=models.EmailField()
   sex=models.CharField(max_length=10)
   school=models.CharField(max_length=30)
   aoi=models.CharField(max_length=500)
   institution=models.CharField(max_length=500)
   designation=models.CharField(max_length=300)

class Progress(PolymorphicModel):
   level=models.IntegerField()
   name=models.CharField(max_length=40)
   scholar=models.ForeignKey(Scholar)
   current=models.BooleanField(default=False)
   result=models.CharField(max_length=5)
   
class DC(Progress):
   date=models.DateField(null=True)
   time=models.TimeField()
   comments=models.CharField(max_length=500)

class Coursework(Progress):
   pass

class Others(Progress):
   date=models.DateTimeField(null=True)
   marks=models.IntegerField(default=0)
   comments=models.CharField(max_length=500)

class Thesis(Progress):
   date=models.DateField(null=True)
   comments=models.CharField(max_length=30)
   fees=models.CharField(max_length=5)
   datePaid=models.DateField(null=True)

class Zero(Progress):
   presented=models.DateField(null=True)
   fees=models.CharField(max_length=5)
   datePaid=models.DateField(null=True)

class Publications(models.Model):
   title=models.CharField(max_length=1000)
   name=models.CharField(max_length=1000)
   date=models.CharField(max_length=10)
   supervisors=models.ManyToManyField(Supervisor)
   scholars=models.ManyToManyField(Scholar)

class Announcement(models.Model):
  title=models.CharField(max_length=200)
  body=models.CharField(max_length=1000)
  adate=models.DateField(null=True,blank=True)

class Message(models.Model):
  head=models.CharField(max_length=100)
  body=models.CharField(max_length=1000)
  date=models.DateTimeField(default=datetime.now)
  scholar=models.ForeignKey(Scholar)
  unread=models.BooleanField(default=False)
  supervisorText=models.ForeignKey(Supervisor,related_name='supervisorText')
  deanText=models.ForeignKey(Supervisor,related_name='deanText')

class Comments(models.Model):
  content=models.CharField(max_length=500)
  date=models.DateTimeField(default=datetime.now)
  scholar=models.ForeignKey(Scholar)
  supervisorText=models.ForeignKey(Supervisor,related_name='supervisorComment')
  deanText=models.ForeignKey(Supervisor,related_name='deanComment')
  message=models.ForeignKey(Message)

class SupMess(models.Model):
  head=models.CharField(max_length=100)
  body=models.CharField(max_length=1000)
  regno=models.CharField(max_length=17)
  mid=models.CharField(max_length=15)

class Subject(models.Model):
  name=models.CharField(max_length=100)
  code=models.CharField(max_length=20)

class Subjected(Subject):
   datePassed=models.DateField(null=True)
   marks=models.IntegerField()
   status=models.CharField(max_length=10)
   course=models.ForeignKey(Coursework)

class DCMembers(models.Model):
   scholar=models.OneToOneField(Scholar)
   members=models.ManyToManyField(Supervisor)