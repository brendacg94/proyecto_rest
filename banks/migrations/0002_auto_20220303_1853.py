# Generated by Django 3.2.12 on 2022-03-04 00:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('banks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movement',
            name='Bank_account',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='bank_accounts', to='banks.bank_account', verbose_name='Cuenta de Banco'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movement',
            name='creation_movement',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]