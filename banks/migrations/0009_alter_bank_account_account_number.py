# Generated by Django 3.2.12 on 2022-03-17 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banks', '0008_auto_20220316_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank_account',
            name='account_number',
            field=models.BigIntegerField(unique=True, verbose_name='Número de cuenta'),
        ),
    ]