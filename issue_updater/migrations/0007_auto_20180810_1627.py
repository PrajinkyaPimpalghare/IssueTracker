# Generated by Django 2.0.7 on 2018-08-10 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issue_updater', '0006_auto_20180810_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportpost',
            name='last_updated',
            field=models.TextField(default='2018-08-10 16:27:29'),
        ),
    ]