# Generated by Django 4.2.4 on 2024-01-30 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UTRADE', '0004_alter_userprofile_wallet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='wallet',
        ),
    ]
