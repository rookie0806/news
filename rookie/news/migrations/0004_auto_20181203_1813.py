# Generated by Django 2.0.7 on 2018-12-03 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20181203_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspaper',
            name='Percentage',
            field=models.FloatField(default=0),
        ),
    ]
