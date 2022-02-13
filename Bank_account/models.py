from django.db import models
from users.models import Usuario
from Bank.models import Bank

# Create your models here.

class Bank_account(models.Model):
    id = models.AutoField(primary_key = True)
    account_number = models.CharField('Número de cuenta', max_length = 255, unique = True, blank = False, null = False)
    balance = models.DecimalField('Saldo', max_digits=10, decimal_places=2,null = False)
    id_user = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name = 'Usuario')
    id_bank = models.ForeignKey(Bank, on_delete=models.CASCADE, verbose_name = 'Banco')

    class Meta:
        verbose_name = 'Cuenta de Banco'
        verbose_name_plural = 'Cuentas de Banco'

    def __str__(self):
        return self.account_number