# Generated by Django 2.2.3 on 2022-03-14 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0007_auto_20220314_0926'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='headimg',
        ),
    ]
