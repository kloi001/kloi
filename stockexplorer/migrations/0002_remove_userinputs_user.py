# Generated by Django 3.0.3 on 2020-03-15 05:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stockexplorer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinputs',
            name='user',
        ),
    ]
