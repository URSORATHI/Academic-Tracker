# Generated by Django 3.1.7 on 2021-05-01 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_subject_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='email',
            field=models.CharField(default='', max_length=100),
        ),
    ]
