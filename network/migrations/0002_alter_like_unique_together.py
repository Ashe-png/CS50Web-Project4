# Generated by Django 4.2.1 on 2023-05-12 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('userl', 'post')},
        ),
    ]