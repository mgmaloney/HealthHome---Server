# Generated by Django 4.2.10 on 2024-02-18 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthhomeapi', '0002_user_credential'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(default=None, max_length=7, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='sex',
            field=models.CharField(default=None, max_length=7, null=True),
        ),
    ]