from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *


def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for error in errors.values():
            messages.error(request, error)
        return redirect('/')

    hashedPw = bcrypt.hashpw(
        request.POST['password'].encode(), bcrypt.gensalt()).decode()
    newUser = User.objects.create(
        firstName=request.POST['firstName'],
        lastName=request.POST['lastName'],
        email=request.POST['email'],
        password=hashedPw
    )
    request.session['userId'] = newUser.id
    return redirect('/success')


def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        userLogin = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), userLogin.password.encode()):
            request.session['userId'] = userLogin.id
            return redirect('/success')
        messages.error(request, 'Invalid Credentials')
        return redirect('/')
    messages.error(request, "User does not exist")
    return redirect('/')


def success(request):
    if 'userId' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['userId'])
    context = {
        'user': user
    }
    return render(request, 'success.html', context)


def logout(request):
    request.session.clear()
    return redirect('/')
