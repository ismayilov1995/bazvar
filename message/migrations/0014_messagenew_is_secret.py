# Generated by Django 2.2.7 on 2019-11-25 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0013_messagelike'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagenew',
            name='is_secret',
            field=models.BooleanField(default=False),
        ),
    ]
