# Generated by Django 2.2.2 on 2019-06-20 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("notes", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="note",
            name="title",
            field=models.CharField(max_length=60, unique=True),
        )
    ]
