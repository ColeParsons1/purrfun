# Generated by Django 4.0.2 on 2022-02-15 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_post_islike'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='post',
        ),
        migrations.AddField(
            model_name='message',
            name='post_id',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
