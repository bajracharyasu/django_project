# Generated by Django 4.2.1 on 2023-05-18 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MindsetApp', '0006_output'),
    ]

    operations = [
        migrations.AlterField(
            model_name='output',
            name='always',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='output',
            name='none',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='output',
            name='often',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='output',
            name='sometimes',
            field=models.IntegerField(null=True),
        ),
    ]
