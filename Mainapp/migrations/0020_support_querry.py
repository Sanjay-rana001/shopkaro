# Generated by Django 4.2 on 2023-07-01 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mainapp', '0019_checkoutproducts_qty_checkoutproducts_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='Support_Querry',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=50)),
                ('phone', models.CharField(max_length=15)),
                ('subject', models.CharField(max_length=50)),
                ('message', models.TextField(max_length=200)),
                ('status', models.IntegerField(choices=[(1, 'Active'), (2, 'Resolved')], default=1)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
