# Generated by Django 4.0.2 on 2022-03-04 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_post_caption_post_isoriginalpost_post_isquotepost_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='Image2',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='post',
            name='Image3',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='post',
            name='Image4',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
