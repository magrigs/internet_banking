# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class user(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_level_id = models.CharField(max_length=255, default = "", unique=True)
    user_username = models.CharField(max_length=255, default = "", unique=True)
    user_password = models.CharField(max_length=20, default = "")
    user_name = models.CharField(max_length=255, default = "")
    user_account_no = models.CharField(max_length=255, default = "")
    user_email = models.CharField(max_length=255, default = "")
    user_mobile = models.CharField(max_length=255, default = "")
    user_aadhar = models.CharField(max_length=255, default = "")

    user_ifsc_code = models.CharField(max_length=255, default = "")
    def __str__(self):
        return self.user_name

class state(models.Model):
    state_id = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=255, default = "")
    def __str__(self):
        return self.state_name

class role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_title = models.CharField(max_length=255, default = "")
    role_description = models.TextField(default = "")
    def __str__(self):
        return self.state_name

class city(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=255, default = "")
    def __str__(self):
        return self.city_name

class country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=255, default = "")
    def __str__(self):
        return self.country_name
