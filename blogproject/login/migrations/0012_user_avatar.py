# Generated by Django 2.2.3 on 2022-03-14 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0011_remove_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.FileField(blank=True, upload_to='avatar/%Y%m%d/'),
        ),
    ]
