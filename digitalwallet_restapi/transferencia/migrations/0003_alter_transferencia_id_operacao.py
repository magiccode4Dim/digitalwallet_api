# Generated by Django 4.1.3 on 2024-02-16 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operacao', '0002_operacao_valor'),
        ('transferencia', '0002_remove_transferencia_valor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transferencia',
            name='id_operacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='operacao.operacao', unique=True),
        ),
    ]