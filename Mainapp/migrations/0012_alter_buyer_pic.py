# Generated by Django 4.2 on 2023-06-26 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mainapp', '0011_alter_buyer_addressline1_alter_buyer_addressline2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer',
            name='pic',
            field=models.FileField(blank=True, default='', null=True, upload_to='buyers'),
        ),
    ]
