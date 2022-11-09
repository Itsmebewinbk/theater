# Generated by Django 4.1.3 on 2022-11-09 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Admin", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="age",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="gender",
            field=models.CharField(
                choices=[
                    ("male", "male"),
                    ("female", "female"),
                    ("not specified", "not specified"),
                ],
                default="not specified",
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="image"),
        ),
        migrations.AlterField(
            model_name="user",
            name="mobile",
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="name",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]