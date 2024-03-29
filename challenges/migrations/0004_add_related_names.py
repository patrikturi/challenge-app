# Generated by Django 3.0.14 on 2021-05-01 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0003_endomondo_id_to_external_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competitor',
            name='display_name',
            field=models.CharField(blank=True, help_text='Optional, name will be parsed form Endomondo if not specified', max_length=100),
        ),
        migrations.AlterField(
            model_name='competitor',
            name='teams',
            field=models.ManyToManyField(blank=True, related_name='competitors', to='challenges.Team'),
        ),
        migrations.AlterField(
            model_name='stats',
            name='challenge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to='challenges.Challenge'),
        ),
        migrations.AlterField(
            model_name='stats',
            name='competitor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to='challenges.Competitor'),
        ),
        migrations.AlterField(
            model_name='team',
            name='challenge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='challenges.Challenge'),
        ),
    ]
