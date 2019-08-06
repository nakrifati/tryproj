# Generated by Django 2.2.4 on 2019-08-06 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0005_auto_20190805_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rule',
            name='rule_value',
            field=models.TextField(default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='name',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
