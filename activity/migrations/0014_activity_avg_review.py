# Generated by Django 2.1.3 on 2019-03-07 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0013_auto_20190305_2309'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='avg_review',
            field=models.FloatField(null=True),
        ),
    ]