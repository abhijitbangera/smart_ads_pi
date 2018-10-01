# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User


from django.db import models
import main_app.settings as settings
# Create your models here.
class adsDetails(models.Model):


    #client_id=models.ForeignKey(User, unique=True,on_delete=models.CASCADE)
    client_id = models.CharField('Client ID', max_length=300,default="",blank= True)
    header = models.CharField('Header text', max_length=300,default="",blank= True)
    left_top = models.CharField('Ad-1: Top Left', max_length=200,default="",blank= True)
    left_bottom = models.CharField('Ad-2: Bottom Left', max_length=200,default="",blank= True)
    right_top = models.CharField('Ad-3: Top Right', max_length=200,default="",blank= True)
    right_bottom = models.CharField('Ad-4: Bottom Right', max_length=200,default="",blank= True)
    footer = models.CharField('Footer Text', max_length=300,default="",blank= True)
    update_flag = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return str(self.client_id)