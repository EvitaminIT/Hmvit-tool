from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser    

# Create your models here.

# class am(BaseUserManager):
#     def create_user(self, username, email, password=None, **kwargs):
#         if username is None: raise ValueError('username is required')
#         if email is None: raise ValueError('email is required')
#         # if password is None:raise ValueError('password is required')
#         user = self.model(email = self.normalize_email(email),username = username)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, email, password, *kwargs):
#         user = self.create_user(email = self.normalize_email(email),username = username)
#         user.is_admin = True
#         user.is_staff = True
#         user.is_superuser = True
#         user.set_password(password)
#         user.save(using=self._db)
#         return user




class am(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        # if username is None: raise ValueError('username is required')
        if email is None: raise ValueError('email is required')
        # if password is None:raise ValueError('password is required')
        user = self.model(email = self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, *kwargs):
        user = self.create_user(email = self.normalize_email(email))
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user

class Users(AbstractBaseUser):

    email = models.EmailField(null=False, unique=True, blank=False)
    username = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=100, null=False)
    user_role = models.CharField(max_length=100, null=False, default='-')
    user_token = models.CharField(max_length=100, null=False, default='-')
    department = models.CharField(max_length=100, null=False, default='-')
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = am()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.name
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return True
    



class toolLink(models.Model):
    tool = models.CharField(max_length=100, null=False)
    jscode = models.TextField(null=False)
    csscode = models.TextField(null=False)
    department = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.tool