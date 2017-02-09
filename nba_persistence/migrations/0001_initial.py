# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-09 06:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GamePlayerBoxScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=100)),
                ('explanation', models.CharField(default=None, max_length=100)),
                ('seconds_played', models.BigIntegerField(default=0)),
                ('field_goals_made', models.BigIntegerField(default=0)),
                ('field_goals_attempted', models.BigIntegerField(default=0)),
                ('three_point_field_goals_made', models.BigIntegerField(default=0)),
                ('three_point_field_goals_attempted', models.BigIntegerField(default=0)),
                ('free_throws_made', models.BigIntegerField(default=0)),
                ('free_throws_attempted', models.BigIntegerField(default=0)),
                ('offensive_rebounds', models.BigIntegerField(default=0)),
                ('defensive_rebounds', models.BigIntegerField(default=0)),
                ('assists', models.BigIntegerField(default=0)),
                ('steals', models.BigIntegerField(default=0)),
                ('blocks', models.BigIntegerField(default=0)),
                ('turnovers', models.BigIntegerField(default=0)),
                ('personal_fouls', models.BigIntegerField(default=0)),
                ('plus_minus', models.BigIntegerField(default=0)),
                ('game_player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.GamePlayer')),
            ],
        ),
    ]