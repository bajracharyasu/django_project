# Generated by Django 4.2.1 on 2023-05-19 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MindsetApp', '0009_rename_answer_output_always_output_none_output_often_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='output',
            name='prediction',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
