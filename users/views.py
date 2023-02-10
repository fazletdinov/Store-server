from django.shortcuts import render, redirect
from django.contrib.auth import (authenticate,
                                 login as login_base,
                                 logout as logout_base)
from django.contrib import messages

from .forms import UserLoginForm, SignUpFrom, UserProfileForm
from products.models import Basket


def login(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(request, username=email, password=password)
        if user:
            login_base(request, user)
            return redirect('home')

    context = {'form': form}

    return render(request, 'users/login.html', context=context)


def signup(request):
    form = SignUpFrom(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Поздравляем, Вы успешно зарегистрировались!")
        return redirect('users:login')

    context = {'form': form}
    return render(request, 'users/signup.html', context=context)


def profile(request):
    form = UserProfileForm(request.POST or None,
                           request.FILES or None,
                           instance=request.user)
    if form.is_valid():
        form.save()
    baskets = Basket.objects.all()
    context = {'form': form, 'baskets': baskets}
    return render(request, 'users/profile.html', context=context)


def logout(request):
    logout_base(request)
    return redirect('home')