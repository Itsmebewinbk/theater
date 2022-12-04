from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser,PermissionsMixin
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager

GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
        ('not specified', 'not specified'),
    )
USER_TYPE = (
    ('customer', 'Customer'),
    ('theater', 'Theater')
)

class Manager(UserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields['is_superuser'] = True
        super(Manager, self).create_superuser(username, email, password,**extra_fields)
        
class CustomUser(AbstractUser):
    image=models.ImageField(upload_to="image",null=True,blank=True)
    mobile=models.CharField(max_length=12,null=True,blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=100,default='not specified')
    name = models.CharField(max_length=200,null=True,blank=True)
    age = models.IntegerField(null=True,blank=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    usertype = models.CharField(choices=USER_TYPE, max_length=50,default="admin")
    def _str_(self):
        return self.name
    objects = Manager()
# class BaseUser(AbstractBaseUser,PermissionsMixin):
#     first_name=models.CharField(max_length=25)
#     last_name=models.CharField(max_length=25)
#     email = models.EmailField( unique=True,verbose_name="email")
#     GENDER_CHOICES = (
#         ('male', 'male'),
#         ('female', 'female'),
#         ('not specified', 'not specified'),
#     )
#     is_customer = models.BooleanField('Is Customer',default=False)
#     is_theatre = models.BooleanField('Is Theatre',default=False)
#     is_superuser = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     gender = models.CharField(choices=GENDER_CHOICES,max_length=100)
#     age = models.IntegerField()
#     mobile = models.CharField(max_length=12)
#     address = models.TextField()
#     CHOICE = ('Admin', 'Admin'), ('Customer', 'Customer'), ('Theater', 'Theater')
#     usertype = models.CharField(choices=CHOICE,max_length=50)
#     USERNAME_FIELD="email"
#     REQUIRED_FIELDS = []

