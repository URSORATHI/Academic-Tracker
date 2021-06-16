from django.db import models
from django.conf import settings

# Create your models here.
User = settings.AUTH_USER_MODEL
    

class student(models.Model):
     name = models.CharField(max_length=30)
    
    
class subject(models.Model):
     email = models.CharField(max_length=100, default="")    
     name = models.ManyToManyField('StudentsR')
     subjectname = models.CharField(max_length=30)
     attendance = models.PositiveIntegerField(null=True, default=0)
     total_lectures = models.PositiveIntegerField(null=True, default=0)
     marks = models.PositiveIntegerField(null=True)
     total_marks = models.PositiveIntegerField(null=True) 

class attendance(models.Model):
    name = models.CharField(max_length=50)
    population = models.CharField(max_length=10,null=True) 

class StudentsR(models.Model):
    username = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    password = models.CharField(max_length=50)

class AdminR(models.Model):
    username1 = models.CharField(max_length=122)
    email1 = models.CharField(max_length=122)
    password1 = models.CharField(max_length=50)
    
class adminsubject(models.Model):
     email = models.CharField(max_length=100, default="", null=True)  
     subjectname = models.CharField(max_length=30)
     total_lectures = models.PositiveIntegerField(null=True)
    
#name = models.ManyToManyField('student')
#name = models.ForeignKey(User,on_delete=models.CASCADE,null=True)