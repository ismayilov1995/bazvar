# Generated by Django 2.2.7 on 2019-11-23 20:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0011_auto_20191124_0019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagenew',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender_n', to=settings.AUTH_USER_MODEL),
        ),
    ]
