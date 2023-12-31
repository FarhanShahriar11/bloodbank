# Generated by Django 4.2.4 on 2023-08-19 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_rename_is_fullfilled_request_is_fulfilled'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='patient_age',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='request',
            name='patient_name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='request',
            name='reason',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
