# Generated by Django 2.1.3 on 2019-03-29 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0014_activity_avg_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='origin',
            field=models.CharField(default='n', max_length=1),
        ),
    ]
