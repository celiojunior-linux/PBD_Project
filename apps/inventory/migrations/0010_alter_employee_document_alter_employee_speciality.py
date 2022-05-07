# Generated by Django 4.0.4 on 2022-05-07 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_alter_employee_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='document',
            field=models.CharField(max_length=11, unique=True, verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='speciality',
            field=models.CharField(max_length=100, verbose_name='especialidade'),
        ),
    ]