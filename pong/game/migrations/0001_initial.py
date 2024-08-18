# Generated by Django 5.0.7 on 2024-07-31 16:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('total_match', models.PositiveSmallIntegerField(default=0)),
                ('total_win', models.PositiveSmallIntegerField(default=0)),
                ('p_win', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('m_score_match', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('m_score_adv_match', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('best_score', models.PositiveSmallIntegerField(default=0)),
                ('m_nbr_ball_touch', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('total_duration', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('m_duration', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('num_participated_tournaments', models.PositiveSmallIntegerField(default=0)),
                ('num_won_tournaments', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Tournoi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('nbr_player', models.PositiveSmallIntegerField()),
                ('date', models.DateField()),
                ('winner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='game.player')),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score_player1', models.PositiveSmallIntegerField()),
                ('score_player2', models.PositiveSmallIntegerField()),
                ('nbr_ball_touch_p1', models.PositiveIntegerField()),
                ('nbr_ball_touch_p2', models.PositiveIntegerField()),
                ('duration', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('is_tournoi', models.BooleanField()),
                ('player1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_as_player1', to='game.player')),
                ('player2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_as_player2', to='game.player')),
                ('winner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='won_matches', to='game.player')),
                ('tournoi', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='matches', to='game.tournoi')),
            ],
        ),
    ]
