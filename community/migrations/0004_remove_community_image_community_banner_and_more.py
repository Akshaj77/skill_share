# Generated by Django 5.0.4 on 2024-05-17 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("community", "0003_community_description_community_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="community",
            name="image",
        ),
        migrations.AddField(
            model_name="community",
            name="banner",
            field=models.ImageField(
                blank=True, null=True, upload_to="community/banner/"
            ),
        ),
        migrations.AddField(
            model_name="community",
            name="profile_image",
            field=models.ImageField(
                blank=True, null=True, upload_to="community/profile_image/"
            ),
        ),
    ]
