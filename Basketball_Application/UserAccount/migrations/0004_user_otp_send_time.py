# Generated by Django 5.2.3 on 2025-06-26 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserAccount', '0003_user_otp_secret_alter_user_is_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='otp_send_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
