# Generated by Django 3.2.12 on 2022-03-29 03:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20220321_1659'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usuario',
            options={'permissions': (('is_teacher', 'Is Teacher'), ('is_student', 'Is Student'))},
        ),
    ]
