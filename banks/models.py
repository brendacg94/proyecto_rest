from django.db import models
from users.models import Usuario

# Create your models here.

class Bank(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField('Nombre', max_length = 255, blank = False, null = False)

    class Meta:
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'

    def __str__(self):
        return self.name

class Bank_account(models.Model):
    id = models.AutoField(primary_key = True)
    account_number = models.CharField('Número de cuenta', max_length = 255, unique = True, blank = False, null = False)
    balance = models.DecimalField('Saldo', max_digits=10, decimal_places=2, null = False)
    account_type = models.CharField('Tipo de cuenta', max_length = 255, blank = False, null = False)
    id_user = models.ForeignKey(Usuario, related_name='bankaccounts', on_delete=models.CASCADE, verbose_name = 'Usuario')
    id_bank = models.ForeignKey(Bank, related_name = 'banks', on_delete=models.CASCADE, verbose_name = 'Banco')

    class Meta:
        verbose_name = 'Cuenta de Banco'
        verbose_name_plural = 'Cuentas de Banco'

    def __str__(self):
        return f'{self.account_number},{self.balance},{self.account_type}'

class Movement(models.Model):
    id = models.AutoField(primary_key = True)
    quantity = models.DecimalField('Cantidad', max_digits=10, decimal_places=2, null = False)
    #fecha = models.CharField('Nombre', max_length = 255, blank = False, null = False)
    account_type = models.CharField('Tipo de movimiento', max_length = 255, null = False)

    class Meta:
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'

    def __str__(self):
        return f'{self.quantity},{self.account_type}'
