# Generated by Django 4.1.3 on 2024-03-10 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agente', '0007_alter_agente_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agente',
            name='token',
            field=models.CharField(default='nulltoken', max_length=45),
        ),
    ]
