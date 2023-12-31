# Generated by Django 4.2.4 on 2023-08-19 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_rename_blood_group_profile_group_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='reciever',
        ),
        migrations.AddField(
            model_name='donation',
            name='reciever',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recieves', to='app.profile'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='donor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donations', to='app.profile'),
        ),
    ]
