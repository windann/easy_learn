# Generated by Django 2.1.7 on 2019-05-20 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.CharField(max_length=400, verbose_name='Описание курса'),
        ),
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Название курса'),
        ),
    ]
