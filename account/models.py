# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class AppUser(models.Model):
	user = models.OneToOneField(User, related_name='app_user')
	fb_id = models.CharField(max_length=100)
	access_token = models.TextField()

class FBPages(models.Model):
	user = models.ForeignKey(User, related_name='page')
	name = models.CharField(max_length=100)
	page_id = models.CharField(max_length=100)
	category = models.CharField(max_length=100)
	access_token = models.TextField()
	