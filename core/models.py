from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django_resized import ResizedImageField 

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password,**extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError('Password is not provided')

        user = self.model(
            email = self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user(email, password,**extra_fields)
    

class User(AbstractBaseUser,PermissionsMixin):

    email =  models.EmailField(('email address'), unique=True)
    username = models.CharField(max_length=150,null=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    class Meta:
        verbose_name_plural = "Accounts"


class Image(models.Model):

    user = models.ForeignKey('User', on_delete=models.CASCADE)
    compressed_image = ResizedImageField(size=[800, 600], upload_to='images/', quality=85, force_format='WEBP')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Images"



