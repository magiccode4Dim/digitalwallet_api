# Generated by Django 4.1.3 on 2024-01-30 20:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('operacao', '0002_operacao_valor'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='operacaoOPT',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('optcode', models.IntegerField(unique=True)),
                ('id_operacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='operacao.operacao')),
            ],
        ),
        migrations.CreateModel(
            name='accontValidationOTP',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('optcode', models.IntegerField(unique=True)),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
