from typing import Any, Dict

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from core.mixins.mixin import TitleMixin
from products.models import Basket

from .forms import SignUpFrom, UserLoginForm, UserProfileForm
from .models import EmailVerification

User = get_user_model()


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Store - Авторизация'


class SignUpCreateView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    template_name = 'users/signup.html'
    form_class = SignUpFrom
    success_url = reverse_lazy('users:login')
    success_message = "Поздравляем, Вы успешно зарегистрировались!"
    title = 'Store - Регистрация'


class UserProfileView(TitleMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')
    title = 'Store - Личный кабинет'

    # def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
    #     context = super().get_context_data(**kwargs)
    #     context['baskets'] = Basket.objects.filter(user=self.object)
    #     return context

    def get_object(self, queryset=None):
        object = self.request.user
        return object


class EmailVerificztionView(TitleMixin, TemplateView):
    title = 'Store - Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args: Any, **kwargs: Any):
        code = self.kwargs.get('code')
        user = get_object_or_404(User, email=self.kwargs.get('email'))
        email_verification = get_object_or_404(EmailVerification,
                                               user=user, code=code)
        if email_verification and not email_verification.is_expired:
            user.is_verify = True
            user.save()
        else:
            return redirect('home')
        return super().get(request, *args, **kwargs)

# def logout(request):
#     logout_base(request)
#     return redirect('home')


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

# def login(request):
#     form = UserLoginForm(request.POST or None)
#     if form.is_valid():
#         email = form.cleaned_data['email']
#         password = form.cleaned_data['password']
#         user = authenticate(request, username=email, password=password)
#         if user:
#             login_base(request, user)
#             return redirect('home')

#     context = {'form': form}

#     return render(request, 'users/login.html', context=context)
