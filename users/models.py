from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Permission, Group, PermissionsMixin

# Create your models here.

class UsuarioManager(BaseUserManager):

    def create_user(self,email,names,last_names, password = None):
        if not email:
            raise ValueError('¡El usuario debe tener un correo electrónico!')

        usuario = self.model(
            email = self.normalize_email(email), 
            names = names, 
            last_names = last_names
        )

        # Encripta la contraseña y la guarda en ese mismo campo
        usuario.set_password(usuario.password)
        usuario.save(using=self._db)
        return usuario 

    def create_superuser(self,email,names,last_names,password = None):
        usuario = self.create_user(
            email, 
            names = names, 
            last_names = last_names,
            password = password
        )

        usuario.admin_user = True
        usuario.save(using=self._db)
        return usuario 

class Usuario(AbstractBaseUser,  PermissionsMixin):
   # username = models.CharField('Nombre de usuario', unique = true, max_length = 100)
    email = models.EmailField('Correo electrónico', unique = True, max_length = 254)
    names = models.CharField('Nombres', max_length = 255, blank = False, null = False)
    last_names = models.CharField('Apellidos', max_length = 255, blank = False, null = False)
    active_user = models.BooleanField(default = True) # todo usuario que tenga este campo en true puede iniciar sesion
    admin_user = models.BooleanField(default = False) # identificar que usuario va poder iniciar sesion en el administrador de django y que usuario no
    objects = UsuarioManager()

    # Hace referencia al parametro unico que va a diferenciar al usuario, que siempre va a ser requerido
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['names','last_names']

    def __str__(self):
        return f'{self.names},{self.last_names}'

    # Verifica si un usuario es administrador o no 
    @property 
    def is_staff(self):
        return self.admin_user




    

