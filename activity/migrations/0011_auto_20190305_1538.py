# Generated by Django 2.1.3 on 2019-03-05 23:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0010_auto_20190305_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='created',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activity',
            name='modified',
            field=models.DateField(auto_now=True),
        ),
    ]
