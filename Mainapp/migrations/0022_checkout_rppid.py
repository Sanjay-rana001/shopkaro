# Generated by Django 4.2 on 2023-07-02 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mainapp', '0021_buyer_otp_alter_checkout_paymentstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='rppid',
            field=models.CharField(default='', max_length=30),
        ),
    ]
