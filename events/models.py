from django.db import models
import datetime
from django.contrib.auth.models import User
# Create your models here.

class Event(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='event')
    image = models.ImageField(upload_to='events/')
    title = models.CharField(max_length=256)
    date = models.DateTimeField()
    location = models.CharField(max_length=256)
    price = models.FloatField()

    def __str__(self):
        return f"{self.title} - {self.date} - {self.price}"
    
    @property
    def month(self):
        return self.date.strftime("%b").upper()

    @property
    def day(self):
        return self.date.day
    
    @property
    def date_text(self):
        return self.date.strftime("%A, %I%p")


'''
event.

image
title
month
day
date_text
location
price
'''