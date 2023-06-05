# Generated by Django 4.2.1 on 2023-05-18 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MindsetApp', '0008_rename_always_output_answer_remove_output_none_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='output',
            old_name='answer',
            new_name='always',
        ),
        migrations.AddField(
            model_name='output',
            name='none',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='output',
            name='often',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='output',
            name='sometimes',
            field=models.IntegerField(null=True),
        ),
    ]