# Generated by Django 4.2.4 on 2023-08-19 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='blood_group',
            new_name='group',
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_donated',
            field=models.DateField(blank=True, null=True),
        ),
    ]
