# Generated by Django 4.1.3 on 2024-02-17 07:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operacao', '0002_operacao_valor'),
        ('levantamento', '0003_alter_levantamento_id_operacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='levantamento',
            name='id_operacao',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='operacao.operacao'),
        ),
    ]
