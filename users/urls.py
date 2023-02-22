from django.urls import path
from django.contrib.auth.views import LogoutView

from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('signup/', views.SignUpCreateView.as_view(), name='signup'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('email-verify/<str:email>/<uuid:code>/',
         views.EmailVerificztionView.as_view(), name='email_verify')
]
