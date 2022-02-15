from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.timezone import now


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None):
        if not email:
            raise ValueError("There are unfilled fields")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True, verbose_name="ユーザID")
    email = models.EmailField(max_length=255, unique=True, verbose_name="メールアドレス")
    company = models.CharField(null=True, max_length=255, verbose_name="会社名")
    address = models.CharField(null=True, max_length=255, verbose_name="住所")
    tel = models.CharField(null=True, max_length=20, verbose_name="電話番号")
    name = models.CharField(null=True, max_length=255, verbose_name="氏名")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    last_login = models.CharField(max_length=100, default=now, verbose_name="最終ログイン日")

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ["last_login"]
        return []

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name_plural = "ユーザ"
