# Generated by Django 2.1.3 on 2019-03-01 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0006_activity_pic_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='pic_url',
            field=models.URLField(blank=True, default='static/images/default.png'),
        ),
    ]
