from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login as login_base
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user:
                login_base(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = AuthenticationForm()

    context = {'form': form}

    return render(request, 'users/login.html', context=context)


def registration(request):
    return render(request, 'users/signup.html')
