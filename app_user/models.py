from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser):
    id = models.IntegerField(primary_key=True, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()
     """
    id: IntegerField (Primary key, not editable)
    first_name: CharField (Max length 50)
    last_name: CharField (Max length 50)
    username: CharField (Max length 50, unique)
    """

class Account(models.Model):
    INPUT = 'kirim'
    OUTPUT = 'chiqim'

    CHOICE_INPUT_OUTPUT = [
        (INPUT, 'Input'),
        (OUTPUT, 'Output'),
    ]
    id = models.IntegerField(primary_key=True, editable=False)
    payment_type = models.CharField(max_length=8, choices=CHOICE_INPUT_OUTPUT)
    total_payment = models.FloatField(default=0.0, blank=True, null=True)
    payment_for = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    """
    INPUT: String representing an input payment ('kirim').
    OUTPUT: String representing an output payment ('chiqim').
    CHOICE_INPUT_OUTPUT: List of tuples representing the choices for payment_type.
    id: IntegerField (Primary key, not editable)
    payment_type: CharField (Max length 8, choices between 'Input' and 'Output')
    total_payment: FloatField (Default 0.0, can be blank or null)
    payment_for: CharField (Max length 150)
    created: DateTimeField (Automatically set on creation)
    updated: DateTimeField (Automatically updated on modification)
    owner: ForeignKey to the User model (On delete cascade)
    """
