# Generated by Django 2.1.7 on 2019-05-10 08:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learn_app', '0004_teachergroup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='course',
        ),
    ]
