# Generated by Django 5.2 on 2025-06-17 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_profile_major_remove_profile_nickname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='followings',
            field=models.ManyToManyField(related_name='followers', to='accounts.profile'),
        ),
    ]
