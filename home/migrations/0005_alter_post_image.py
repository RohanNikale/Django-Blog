# Generated by Django 4.0.3 on 2022-05-27 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='rohan', upload_to='static/blogimage'),
        ),
    ]
