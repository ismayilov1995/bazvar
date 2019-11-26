# Generated by Django 2.2.7 on 2019-11-20 17:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=500, verbose_name='Mesaj')),
                ('comment_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='commentr', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Mesajlar',
            },
        ),
    ]