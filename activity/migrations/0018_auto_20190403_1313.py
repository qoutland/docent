# Generated by Django 2.1.3 on 2019-04-03 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0017_auto_20190403_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='event_date',
            field=models.DateField(null=True),
        ),
    ]
