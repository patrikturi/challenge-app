# Generated by Django 3.0.3 on 2020-02-22 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challange', '0002_calories_competitor_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='challange',
            name='endomondo_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='competitor',
            name='endomondo_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
