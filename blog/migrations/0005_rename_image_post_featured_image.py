# Generated by Django 4.1 on 2024-02-02 01:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_likes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='image',
            new_name='featured_image',
        ),
    ]
