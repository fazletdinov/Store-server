from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, phone, password, **extra_fields):
        if not email:
            raise ValueError('Вы не ввели email')
        if not phone:
            raise ValueError('Введите номер телефона')
        email = self.normalize_email(email=email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using='default')
        return user

    def create_user(self, email, phone, password):
        return self._create_user(email, phone, password)

    def create_superuser(self, email, phone, password):
        return self._create_user(email,
                                 phone,
                                 password,
                                 is_superuser=True,
                                 is_admin=True,
                                 is_active=True)
