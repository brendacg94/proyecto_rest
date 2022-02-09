from django.db import models

# Create your models here.

class Bank(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField('Nombre', max_length = 255, blank = False, null = False)

    class Meta:
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'

    def __str__(self):
        return self.name