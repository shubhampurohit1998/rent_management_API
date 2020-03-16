# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser
# from idna import unicode


class User(AbstractUser):
    mobile = models.CharField(max_length=10, blank=True, null=True, unique=True,
                              verbose_name='Contact number')
    profile_picture = models.ImageField(upload_to='profile_pictures/',
                                        blank=True, null=True, verbose_name='Profile picture')
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Gender')
    is_owner = models.BooleanField(default=False, verbose_name="Owner")
    is_customer = models.BooleanField(default=False, verbose_name='Customer')

    def __str__(self):
        return self.first_name


class Property(models.Model):
    PROPERTY_TYPE = [
        ('office', 'Office'),
        ('home', 'Home'),
        ('flat', 'Flat'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Owner")
    price = models.CharField(max_length=30,)
    size = models.CharField(max_length=30,)
    address = models.CharField(max_length=100,)
    p_type = models.CharField(
        max_length=8,
        choices=PROPERTY_TYPE,
    )
    city = models.CharField(max_length=30, null=False, blank=False,)
    description = models.TextField(max_length=150, blank=True, null=True,)
    is_active = models.BooleanField(default=True, )

    class Meta:
        get_latest_by = id

    def __unicode__(self):
        return self.city  # f-string python 3 string concatenation


class Rent(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True,
                             verbose_name="Customer")
    date_on_rent = models.DateField(null=False, verbose_name="Rent start date")
    tenure = models.DateField(blank=True, null=True, verbose_name="Rent period")
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.property


class Picture(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    pic_name = models.ImageField(upload_to='images/')


class Message(models.Model):
    message = models.TextField(max_length=150, blank=False, null=False)
    rent = models.ForeignKey(Rent, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')

    # def __str__(self):
    #     return self.rent.id


class LeaveRequest(models.Model):
    request_accept = models.NullBooleanField()
    rent = models.ForeignKey(Rent, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
