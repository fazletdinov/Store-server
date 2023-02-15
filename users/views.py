from django.shortcuts import render, redirect
from django.contrib.auth import (authenticate,
                                 login as login_base,
                                 logout as logout_base)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from typing import Any, Dict, Optional
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserLoginForm, SignUpFrom, UserProfileForm
from products.models import Basket


User = get_user_model()


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


class SignUpCreateView(CreateView):
    model = User
    template_name = 'users/signup.html'
    form_class = SignUpFrom
    success_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Store - Регистрация'
        return context


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = UserProfileForm

    def get_success_url(self) -> str:
        return reverse_lazy('users:profile', args=(self.object.id))

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Store - Личный кабинет'
        context['baskets'] = Basket.objects.filter(user=self.object)
        return context

    def get_object(self, queryset=None):
        object = User.objects.get(id=self.request.user.id)
        return object


def logout(request):
    logout_base(request)
    return redirect('home')


# def signup(request):
#     form = SignUpFrom(request.POST or None)
#     if form.is_valid():
#         form.save()
#         messages.success(
#             request, "Поздравляем, Вы успешно зарегистрировались!")
#         return redirect('users:login')

#     context = {'form': form}
#     return render(request, 'users/signup.html', context=context)

# @login_required
# def profile(request):
#     form = UserProfileForm(request.POST or None,
#                            request.FILES or None,
#                            instance=request.user)
#     if form.is_valid():
#         form.save()
#         return redirect('users:profile')
#     baskets = Basket.objects.filter(user=request.user)

#     context = {'form': form, 'baskets': baskets}
#     return render(request, 'users/profile.html', context=context)
