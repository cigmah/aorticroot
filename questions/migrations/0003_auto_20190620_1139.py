# Generated by Django 2.2.2 on 2019-06-20 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_auto_20190620_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionchoice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_choice', to='questions.Question'),
        ),
    ]