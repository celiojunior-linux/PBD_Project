# Generated by Django 4.0.4 on 2022-05-07 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0012_company_registration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='distance_tolerance',
            field=models.FloatField(verbose_name='tolerância de distância (km)'),
        ),
        migrations.AlterField(
            model_name='company',
            name='registration',
            field=models.CharField(max_length=255, verbose_name='inscrição estadual'),
        ),
    ]
