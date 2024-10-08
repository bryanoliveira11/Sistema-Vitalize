from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class VitalizeUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='E-mail')
    first_name = models.CharField(
        max_length=150, blank=True, verbose_name='Nome'
    )
    last_name = models.CharField(
        max_length=150, blank=True, verbose_name='Sobrenome')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Alterado em',
    )
    phone_number = PhoneNumberField(
        blank=True, verbose_name='Telefone / Celular'
    )
    is_active = models.BooleanField(
        default=True, verbose_name='Ativo/Inativo',
        help_text='Marque Essa Caixa para Ativar esse Usuário. '
        'Desmarque para Inativar.',
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Acesso a Área Administrativa',
        editable=True,
        help_text='Marque para Permitir '
        'Acesso a Área Administrativa.',

    )
    is_superuser = models.BooleanField(
        default=False, verbose_name='Administrador Vitalize', editable=True,
        help_text='Administrador Vitalize : Marque para dar Todas as '
        'Permissões para Este Usuário na Área Administrativa.',
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}' \
            if self.first_name else self.email

    class Meta:
        verbose_name = 'Usuário Vitalize'
        verbose_name_plural = 'Usuários Vitalize'
