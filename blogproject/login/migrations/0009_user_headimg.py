# Generated by Django 2.2.3 on 2022-03-14 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0008_remove_user_headimg'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='headimg',
            field=models.FileField(default='avatars/default.jpg', upload_to='avatars/'),
        ),
    ]
