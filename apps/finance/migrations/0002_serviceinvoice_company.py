# Generated by Django 4.0.4 on 2022-05-24 01:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_client_company_employee_company'),
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceinvoice',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='inventory.company', verbose_name='empresa'),
            preserve_default=False,
        ),
    ]
