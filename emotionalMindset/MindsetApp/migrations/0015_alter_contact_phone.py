# Generated by Django 4.2.1 on 2023-05-25 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MindsetApp', '0014_alter_contact_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.IntegerField(null=True),
        ),
    ]
