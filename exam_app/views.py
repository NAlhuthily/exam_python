from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
from datetime import datetime
# Create your views here.
def index(request):
    if 'user' in request.session:
        return redirect("/dashboard")
    return render(request, 'login_reg.html')

def register(request):
    errors = Users.objects.validator(request.POST)
    if len(errors)>0:
        for key,val in errors.items():
            messages.error(request,val)
        return redirect("/")
    else:
        if request.method=="POST":
            password=request.POST['password']
            passHash=bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
            user=Users.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],
            password=passHash)
            request.session['user']=user.id
            messages.success(request,"User successfully created")
        return redirect("/dashboard")

def login(request):
    if request.method=="POST":
        user=Users.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user'] = logged_user.id
                messages.success(request,"Successfully logged in")
                return redirect("/dashboard")
            else:
                messages.error(request,"Email or password is not correct")
                return redirect("/")
        else:
            messages.error(request,"Email or password is not correct")
            return redirect("/")

def logout(request):
    request.session.flush()
    return redirect("/")

def dashboard(request):
    if 'user' in request.session:
        user=Users.objects.get(id=request.session['user'])
        context={
            'user':user,
            'all_wish':Wish.objects.all(),
            'all_wish_revers':user.wish.all().order_by('-id')
        }
        return render(request,'home.html',context)
    else:
        return redirect("/")

def new_wish(request):
    if 'user' in request.session:
        context={
            "user":Users.objects.get(id=request.session['user'])
        }
    return render(request,"create_wish.html",context)

def create_wish(request):
    errors = Wish.objects.validator(request.POST)
    if len(errors)>0:
        for key,val in errors.items():
            messages.error(request,val)
        return redirect("/wishes/new")
    else:
        if request.method=="POST":
            user=Users.objects.get(id=request.session['user'])
            wish=Wish.objects.create(item=request.POST["item"],
                desc=request.POST["desc"],wisher=user)
        return redirect("/dashboard")

def stats(request):
    granted_count=0
    pending_count=0
    granted_count_all=0
    user=Users.objects.get(id=request.session['user'])
    all_wishes=Wish.objects.all()
    for i in user.wish.all():
        if i.granted:
            print(i.item)
            granted_count=granted_count+1
        else:
            pending_count=pending_count+1
    for i in all_wishes.all():
        if i.granted:
            granted_count_all=granted_count_all+1
    context={
        'granted_count':granted_count,
        'pending_count':pending_count,
        'granted_count_all':granted_count_all
    }
    return render(request,"stats.html",context)

def edit(request,id):
    context={
        "wish":Wish.objects.get(id=id),
    }
    return render(request,"update_wish.html",context)

def update(request,id):
    wish=Wish.objects.get(id=id)
    errors = Wish.objects.validator(request.POST)
    if len(errors)>0:
        for key,val in errors.items():
            messages.error(request,val,key)
        return redirect(f"/wishes/edit/{id}")
    else:
        if request.method =="POST":
            wish=Wish.objects.get(id=id)
            wish.item=request.POST["item"]
            wish.desc=request.POST["desc"]
            wish.save()
        return redirect("/dashboard")

def delete(request,id):
    wish=Wish.objects.get(id=id)
    wish.delete()
    return redirect("/dashboard")

def granted(request,id):
    wish=Wish.objects.get(id=id)
    wish.granted=True
    wish.date_granted=today=datetime.today().date()
    wish.save()
    return redirect("/dashboard")

def like(request,id):
    wish=Wish.objects.get(id=id)
    user=Users.objects.get(id=request.session['user'])
    wish.user_who_like.add(user)
    return redirect("/dashboard")