from django.db import models
import re


# Create your models here.

class UserManger(models.Manager):
    def reg_validator(self , postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) == 0 :
            errors['first_name-empty'] = " First Name must be filled  ."
        if  len(postData['last_name']) == 0:
            errors['last_name-empty'] = " Last Name must be filled  ."
        if  len(postData['email']) == 0:
            errors['emaill-empty'] = "  email must be filled  ."
        if  len(postData['password']) == 0 :
            errors['password-r-empty'] = " password must be filled  ."
        if  len(postData['confirmation_password']) == 0:
            errors['password-C-empty'] = " Passwoed-C  must be filled  ."   

        if len(postData['first_name']) < 3 :
            errors['first_name'] = " First Name has to be at least 2 characters ."
        if len(postData['last_name']) < 3 :
            errors['last_name'] = "Last Name  has to be at least 2 characters ."
        if len(postData['password']) < 8 :
            errors['password'] = " password has to be at least 8 characters."
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if postData['password'] != postData['confirmation_password']:
            errors['password_no_match'] = 'Your passwords do not match.'
        return errors

    def login_validator(self , postData):
        errors = {}
        if (len(postData['login_email']) ==0):
            errors['login_email'] = "Email address should be filled" 
        if (len(postData['login_password']) ==0):
            errors['login_password'] = "Password address should be filled" 
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['login_email']):
            errors['email'] = "Invalid email address!"
        return errors

class PypieManager(models.Manager):

    def Pypie_validator(self, postData):
        errors = {}
        if len(postData['name']) == 0:
            errors['name'] = 'Please fill out the pypie name field.'
        if len(postData['filling']) == 0:
            errors['filling'] = 'Please fill out the pypie filling  field.'
        if len(postData['crust']) == 0:
            errors['crust'] = 'Please fill out the pypie crust field.'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=65)
    last_name = models.CharField(max_length=65)
    email = models.EmailField()
    password = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManger()

class Pypie(models.Model):
    name = models.CharField(max_length=65)
    filling = models.CharField(max_length=65)
    crust = models.CharField(max_length= 65)
    votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User , related_name="pypies_added" , on_delete=models.CASCADE)
    users_who_votes = models.ManyToManyField(User , related_name = 'liked_pie')
    objects = PypieManager()



def create_user(first_name , last_name , email , password):
    return User.objects.create(first_name = first_name , last_name = last_name , email=email , password = password)

def get_user_id(id):
    return User.objects.get(id=id)


def get_users_list(email):
    return User.objects.filter(email=email)

def create_pie(name , filling , crust , added_by):
    return Pypie.objects.create(name = name , filling = filling , crust = crust , added_by = added_by)

def deletepie(request,id):
    pie_to_delete = Pypie.objects.get(id=id)
    pie_to_delete.delete()
    

def updatepie(request ,pie_id):
    pie_to_edit = Pypie.objects.get(id=pie_id)
    pie_to_edit.name =request.POST['name']
    pie_to_edit.filling = request.POST['filling']
    pie_to_edit.crust = request.POST['crust']
    pie_to_edit.save()