# Generated by Django 4.1.3 on 2024-03-10 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agente', '0006_agente_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agente',
            name='token',
            field=models.CharField(default='', max_length=45),
        ),
    ]
