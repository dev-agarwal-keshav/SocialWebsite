# Generated by Django 3.0.2 on 2020-06-02 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0006_remove_like_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='default.png', upload_to='user_image/Profile'),
        ),
    ]
