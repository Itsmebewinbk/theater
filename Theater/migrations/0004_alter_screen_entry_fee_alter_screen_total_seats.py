# Generated by Django 4.1.3 on 2022-11-13 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Theater", "0003_rename_theater_screen_theater_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="screen",
            name="entry_fee",
            field=models.IntegerField(default=100),
        ),
        migrations.AlterField(
            model_name="screen",
            name="total_seats",
            field=models.IntegerField(default=50),
        ),
    ]
