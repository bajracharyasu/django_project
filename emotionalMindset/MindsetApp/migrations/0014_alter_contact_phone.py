# Generated by Django 4.2.1 on 2023-05-25 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MindsetApp', '0013_contact_alter_chat_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.IntegerField(max_length=200),
        ),
    ]
