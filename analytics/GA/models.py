from django.db import models

# Create your models here.

class Datevssessionsmodel(models.Model):
    date=models.DateField(primary_key=True)
    sessions=models.IntegerField()

class Newvisitormodel(models.Model):
    date=models.DateField(primary_key=True)
    visitor=models.CharField(max_length=20)
    time=models.FloatField()

class Repeatedvisitormodel(models.Model):
    date=models.DateField(primary_key=True)
    visitor=models.CharField(max_length=20)
    time=models.FloatField()
    
   
    


