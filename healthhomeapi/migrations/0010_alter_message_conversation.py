# Generated by Django 4.2.10 on 2024-02-23 02:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('healthhomeapi', '0009_message_conversation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='conversation',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='conversation_messages', to='healthhomeapi.conversation'),
        ),
    ]
