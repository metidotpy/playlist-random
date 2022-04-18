from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.apps import apps
from django.contrib import auth
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group, Permission, PermissionsMixin
from django.core.mail import send_mail
from django.utils import timezone
import os
from random import randint
from django.core.validators import RegexValidator
from django.utils.html import format_html

def split_ext(file):
    base_name = os.path.basename(file)
    name, ext = os.path.splitext(base_name)

    return name, ext

def upload_path(instance, filepath):
    name, ext = split_ext(filepath)
    new_name = randint(0, 999999999)
    final_path = f"avatar/{instance.username}/{instance.id}/{new_name}{ext}"
    return final_path

# Create your models here.


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)

    def with_perm(
        self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    username_validator = RegexValidator(regex=r'^(?=[a-zA-Z0-9_]{1,50}$)(?!.*[_.]{2})[^_.].*[^_.]$', message=_(
        "Enter a valid username. This value may contain only letters, "
        "numbers, and '_' characters."
    ))

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 50 characters or fewer. Letters, digits and '_' only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    avatar = models.ImageField(
        _("Profile photo"),
        default="avatar/default.png",
        upload_to = upload_path,
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_avatar(self):
        return format_html("<img src='{}' width='30' height='30' style='object-fit: cover; border-radius:50%;' />".format(self.avatar.url))


class User(AbstractUser):
    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
