# Generated by Django 4.1.3 on 2024-01-04 21:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deposito', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deposito',
            name='valor',
        ),
    ]