# Generated by Django 2.1.1 on 2018-10-01 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localpi', '0007_remove_adsdetails_client_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='adsdetails',
            name='client_id',
            field=models.CharField(blank=True, default='', max_length=300, verbose_name='Client ID'),
        ),
    ]
