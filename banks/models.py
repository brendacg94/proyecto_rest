from users.models import Usuario
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

class Account_type(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField('Nombre', max_length = 255, blank = False, null = False)

    class Meta:
        verbose_name = 'Tipo de cuenta'
        verbose_name_plural = 'Tipo de cuentas'

    def __str__(self):
        return self.name

class Bank_account(models.Model):
    id = models.AutoField(primary_key = True)
    #account_number = models.CharField('Número de cuenta', max_length = 255, unique = True, blank = False, null = False)
    account_number = models.BigIntegerField('Número de cuenta', unique = True, blank = False, null = False)
    balance = models.DecimalField('Saldo', max_digits=10, decimal_places=2, default = 0)
    #account_type = models.CharField('Tipo de cuenta', max_length = 255, blank = False, null = False)
    id_user = models.ForeignKey(Usuario, related_name='bankaccounts', on_delete=models.CASCADE, verbose_name = 'Usuario')
    id_bank = models.ForeignKey(Bank, related_name = 'banks', on_delete=models.CASCADE, verbose_name = 'Banco')
    id_account_type = models.ForeignKey(Account_type, related_name = 'accounts_type', on_delete=models.CASCADE, verbose_name = 'Tipo de cuenta')

    class Meta:
        verbose_name = 'Cuenta de Banco'
        verbose_name_plural = 'Cuentas de Banco'

    def __str__(self):
        return f'{self.account_number},{self.balance}'

class Movement_type(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField('Nombre', max_length = 255, blank = False, null = False)

    class Meta:
        verbose_name = 'Tipo de movimiento'
        verbose_name_plural = 'Tipo de movimientos'

    def __str__(self):
        return self.name

class Movement(models.Model):
    id = models.AutoField(primary_key = True)
    quantity = models.DecimalField('Cantidad', max_digits=10, decimal_places=2, null = False)
    creation_movement = models.DateTimeField(auto_now_add=True)
    #movement_type = models.CharField('Tipo de movimiento', max_length = 255, null = False)
    available_balance = models.DecimalField('Saldo disponible', max_digits=10, decimal_places=2, default = 0)
    movement_type = models.ForeignKey(Movement_type, related_name = 'movements_type', on_delete=models.CASCADE, verbose_name = 'Tipo de movimiento')
    bank_account = models.ForeignKey(Bank_account, related_name = 'bank_accounts', on_delete=models.CASCADE, verbose_name = 'Cuenta de Banco')

    class Meta:
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'

    def __str__(self):
        return self.quantity


