# Generated by Django 4.1.3 on 2024-02-17 07:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cliente', '0003_alter_cliente_id_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='id_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
