# Generated by Django 4.0.4 on 2022-05-25 00:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_company_manager_company_president'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='manager', to=settings.AUTH_USER_MODEL, verbose_name='gerente'),
        ),
    ]
