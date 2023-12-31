# Generated by Django 4.2 on 2023-06-26 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mainapp', '0010_buyer_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer',
            name='addressline1',
            field=models.CharField(blank=True, default='None', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='addressline2',
            field=models.CharField(blank=True, default='None', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='addressline3',
            field=models.CharField(blank=True, default='None', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='city',
            field=models.CharField(blank=True, default='None', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='pin',
            field=models.CharField(blank=True, default='None', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='state',
            field=models.CharField(blank=True, default='None', max_length=30, null=True),
        ),
    ]
