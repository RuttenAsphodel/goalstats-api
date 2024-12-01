# Generated by Django 4.2.8 on 2024-11-30 23:05

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users_auth', '0009_alter_customuser_fecha_nacimiento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='fecha_nacimiento',
            field=models.DateField(default=datetime.datetime(2024, 11, 30, 20, 5, 56, 48640)),
        ),
        migrations.CreateModel(
            name='PerformanceMetric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meters_covered', models.DecimalField(decimal_places=2, help_text='Metros recorridos durante el encuentro', max_digits=8, validators=[django.core.validators.MinValueValidator(0)])),
                ('goals_scored', models.IntegerField(default=0, help_text='Número de goles anotados', validators=[django.core.validators.MinValueValidator(0)])),
                ('intercepted_passes', models.IntegerField(default=0, help_text='Número de pases interceptados', validators=[django.core.validators.MinValueValidator(0)])),
                ('successful_passes', models.IntegerField(default=0, help_text='Número de pases dados exitosamente', validators=[django.core.validators.MinValueValidator(0)])),
                ('match_date', models.DateTimeField(help_text='Fecha y hora del encuentro')),
                ('suggested_position', models.CharField(blank=True, choices=[('FORWARD', 'Delantero'), ('MIDFIELDER', 'Mediocampista'), ('DEFENDER', 'Defensa'), ('GOALKEEPER', 'Portero')], help_text='Posición sugerida basada en el análisis de rendimiento', max_length=20, null=True)),
                ('performance_score', models.DecimalField(blank=True, decimal_places=2, help_text='Puntuación general de rendimiento', max_digits=5, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('athlete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='performance_metrics', to=settings.AUTH_USER_MODEL)),
                ('sport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='performance_metrics', to='users_auth.discipline')),
            ],
            options={
                'verbose_name': 'Métrica de Rendimiento',
                'verbose_name_plural': 'Métricas de Rendimiento',
                'ordering': ['-match_date'],
            },
        ),
    ]