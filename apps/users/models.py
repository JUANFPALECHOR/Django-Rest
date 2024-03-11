from django.db import models


from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from simple_history.models import HistoricalRecords

# Definición del administrador de usuarios personalizado
class UserManager(BaseUserManager):
    def _create_user(self, username, email, name, last_name, password, is_staff, is_superuser, **extra_fields):
        # Crea y guarda un usuario con los campos proporcionados
        user = self.model(
            username=username,
            email=email,
            name=name,
            last_name=last_name,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Método para crear un usuario estándar
    def create_user(self, username, email, name, last_name, password=None, **extra_fields):
        return self._create_user(username, email, name, last_name, password, False, False, **extra_fields)

    # Método para crear un superusuario
    def create_superuser(self, username, email, name, last_name, password=None, **extra_fields):
        return self._create_user(username, email, name, last_name, password, True, True, **extra_fields)


# Definición del modelo de usuario personalizado
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Campos adicionales según las necesidades de tu aplicación

    # Configuración del administrador de usuarios personalizado
    objects = UserManager()

    # Configuración de historial para realizar un seguimiento de cambios en el modelo
    history = HistoricalRecords()

    # Especifica el campo utilizado como nombre de usuario para autenticación
    USERNAME_FIELD = 'username'
    # Especifica los campos requeridos al crear un superusuario
    REQUIRED_FIELDS = ['email', 'name', 'last_name']

    def __str__(self):
        return self.username



