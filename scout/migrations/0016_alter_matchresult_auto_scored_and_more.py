# Generated by Django 4.0.3 on 2022-04-03 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scout', '0015_rename_auto_ball_matchresult_auto_scored_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchresult',
            name='auto_scored',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='matchresult',
            name='tele_scored',
            field=models.IntegerField(default=0),
        ),
    ]
