from django.db import models
import re
from datetime import datetime
# Create your models here.
class WishManager(models.Manager):
    def validator(self,postData):
        today=datetime.today().date()
        # year=datetime.today().year
        errors={}
        if len(postData['item'])<3:
            errors['item']='Wish should be at lesat 3 charictors'
        if len(postData['desc'])<3:
            errors['desc']='Description must be provided'
        return errors

class UserManager(models.Manager):
    def validator(self,postData):
        errors={}
        NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['first_name'])<2:
            errors['first_name']='First name should be at lesat 2 charictors'
        elif not NAME_REGEX.match(postData['first_name']):
            errors['first_name']='First name should only be letters'
        if len(postData['last_name'])<2:
            errors['last_name']='Last name should be at lesat 2 charictors'
        elif not NAME_REGEX.match(postData['last_name']):
            errors['last_name']='Last name should only be letters'
        if not EMAIL_REGEX.match(postData['email']):                
            errors['email'] = "Invalid email address!"
        if len(postData['password'])<8:
            errors['password']='Password should be at lesat 8 charictors'
        elif postData['password'] != postData['confirm_pw']:
                errors['password'] = 'Confirm PW does not match the password!'
        user=Users.objects.filter(email=postData['email'])
        if user:
            errors['email']='Email is already exist'
        return errors


class Users(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Wish(models.Model):
    item = models.CharField(max_length=45)
    desc= models.TextField()
    granted=models.BooleanField(default=False)
    wisher= models.ForeignKey(Users,related_name="wish",on_delete=models.CASCADE)
    user_who_like=models.ManyToManyField(Users,related_name="liked_wish")
    date_added = models.DateTimeField(auto_now_add=True)
    date_granted = models.DateTimeField(auto_now=True)
    objects= WishManager()
