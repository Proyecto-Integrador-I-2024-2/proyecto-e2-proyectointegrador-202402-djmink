from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Manager para manejar la creación de usuarios y superusuarios
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("El usuario debe tener un correo electrónico")
        user = self.model(
            username=username,
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username=username, email=email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



# Modelo base de usuario
class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


# Perfil común a Freelancers y Companies
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


# Modelo para Freelancers
class Freelancer(Profile):
    portfolio_url = models.URLField(max_length=255, blank=True)
    skills = models.TextField(blank=True)
    
    def __str__(self):
        return f"Freelancer: {self.name}"


# Modelo para Companies
class Company(Profile):
    legal_agent = models.CharField(max_length=255)
    
    def __str__(self):
        return f"Company: {self.name}"
