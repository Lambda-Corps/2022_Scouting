# Generated by Django 4.0.3 on 2022-04-05 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scout', '0016_alter_matchresult_auto_scored_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='matchresult',
            name='climb_height',
        ),
        migrations.RemoveField(
            model_name='matchresult',
            name='tele_scored',
        ),
        migrations.RemoveField(
            model_name='matchresult',
            name='tele_target',
        ),
        migrations.AddField(
            model_name='matchresult',
            name='climb_points',
            field=models.PositiveSmallIntegerField(choices=[('Low Bar', 4), ('Mid Bar', 6), ('High Bar', 10), ('Traversal Bar', 15), ('Failed', 0)], default=0),
        ),
        migrations.AddField(
            model_name='matchresult',
            name='tele_high',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='matchresult',
            name='tele_low',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]