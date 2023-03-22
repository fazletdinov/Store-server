from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from users.managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=50)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    image = models.ImageField(upload_to='users_photo/%Y/%m/%d', blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verify = models.BooleanField(default=False)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self) -> str:
        return f'Emailverification object for {self.user.email}'

    def send_verification_email(self):
        link = reverse('users:email_verify',
                       kwargs={'email': self.user.email,
                               'code': self.code})
        verification_link = f"{settings.DOMAIN_NAME}{link}"
        subject = f"Подтверждение учетной записи для {self.user.email}."
        message = ("Для подверждения учетной записи для {} "
                   "перейдите по ссылке {}".format(self.user.email,
                                                   verification_link))
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return True if now() >= self.expiration else False
