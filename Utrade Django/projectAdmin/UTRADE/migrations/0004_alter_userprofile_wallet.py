# Generated by Django 4.2.4 on 2024-01-30 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UTRADE', '0003_userprofile_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='wallet',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
