# Generated by Django 2.2.3 on 2022-03-14 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_auto_20220314_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='headimg',
            field=models.FileField(default='avatars/default.jpg', upload_to='avatars/'),
        ),
    ]
