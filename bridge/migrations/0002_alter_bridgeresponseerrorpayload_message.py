# Generated by Django 4.0.4 on 2022-05-13 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bridge', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bridgeresponseerrorpayload',
            name='message',
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
    ]
