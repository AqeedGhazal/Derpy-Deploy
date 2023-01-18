from django.shortcuts import render , redirect
from . import models
import bcrypt
from .models import User , Pypie
from django.contrib import messages


# Create your views here.

def index(request):

    return render ( request , 'index.html')

def user_register(request):
    errors = User.objects.reg_validator(request.POST)
    if request.method == 'POST':
        if len(errors) > 0 :
            for key , value in errors.items():
                messages.error(request , value)
                return redirect('/')
        else:
            user = request.POST
            password = user['password']
            PW_hash = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
            models.create_user(user['first_name'] , user['last_name'] , user['email'] , PW_hash)
            return redirect('/')

def user_login(request):
    errors = User.objects.login_validator(request.POST)
    if request.method == 'POST':
        if len(errors) >0 :
            for key, valuee in errors.items():
                messages.error(request ,valuee)
                return redirect('/')
        else:
            users_list = models.get_users_list(request.POST['login_email'])
            if len(users_list)==0 :
                messages.error(request , "please check your Email/Password")
            if not bcrypt.checkpw(request.POST['login_password'].encode(), users_list[0].password.encode()):
                messages.error(request , "please check your password")
                return redirect('/')
            request.session['user_id'] = users_list[0].id
            return redirect('/dashboard')

def success_login(request):
    if 'user_id' not in request.session:
        messages.error(request ,'You must login to view that page')
        return redirect('/')
    else:
        context = {
            "user": models.get_user_id(request.session['user_id']),
            "user_pies":Pypie.objects.filter(added_by =models.get_user_id(request.session['user_id'] )),
        }
        return render(request , 'dashboard.html' , context)

def add_pie(request):
    errors = Pypie.objects.Pypie_validator(request.POST)
    if request.method == "POST":
        if len(errors)> 0 : 
            for key , value in errors.items():
                messages.error(request, value)
            return redirect('/dashboard')
        else:
            pypie = request.POST
            added_by = User.objects.get(id =request.session['user_id'])
            models.create_pie(pypie['name'] , pypie['filling'] , pypie['crust'] ,added_by )
            return redirect('/dashboard')


def delete_Pie(request ,id):
    models.deletepie( request ,id)

    return redirect('/dashboard')


def edit_pie(request,pie_id):
    context = {
        "pypie": Pypie.objects.get(id =pie_id),
        "user": models.get_user_id(request.session['user_id']),
    }
    return render (request , 'editpie.html' , context)

def update_pie (request , pie_id):
    errors = Pypie.objects.Pypie_validator(request.POST)
    if request.method == "POST":
        if len(errors)> 0 : 
            for key , value in errors.items():
                messages.error(request, value)
            return redirect(f'/dashboard/{pie_id}/edit')
        else:
            models.updatepie(request , pie_id)
    return redirect ('/dashboard')

def view_all_pie(request):
    context = {
        "all_pypie": Pypie.objects.all().order_by("-votes"),
    }
    return render(request , 'allpie.html' , context)


def show_pie(request , pie_id):
    
    context = {

        "pypie": Pypie.objects.get(id = pie_id),
        "user" : models.get_user_id(id=request.session['user_id'])
    }
    return render (request , 'showpie.html' , context)

def add_vote(request ,pie_id):
    user = User.objects.get(id = request.session['user_id'])
    pypie = Pypie.objects.get(id = pie_id)
    user.liked_pie.add(pypie)
    pypie.votes += 1
    pypie.save()
    user.save()
    return redirect(f'/show/{pie_id}')

def remove_vote(request ,pie_id):
    user = User.objects.get(id = request.session['user_id'])
    pypie = Pypie.objects.get(id = pie_id)
    user.liked_pie.remove(pypie)
    pypie.votes -= 1 
    pypie.save()
    user.save()
    return redirect(f'/show/{pie_id}')



def user_logout(request):
    request.session.clear()
    return redirect('/')