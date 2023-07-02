# Generated by Django 4.2 on 2023-06-30 19:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Mainapp', '0014_wishlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('paymentMode', models.IntegerField(choices=[(1, 'COD'), (2, 'Net Banking')], default=1)),
                ('paymentStatus', models.IntegerField(choices=[(1, 'done'), (2, 'pending')], default=1)),
                ('orderStatus', models.IntegerField(choices=[(1, 'Order Placed'), (2, 'Ready to Dispatch'), (3, 'Dispatched'), (4, 'Out for delovery'), (5, 'Delivered')], default=1)),
                ('shipping', models.IntegerField()),
                ('final', models.IntegerField()),
                ('date', models.DateTimeField(auto_now=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mainapp.buyer')),
            ],
        ),
        migrations.CreateModel(
            name='CheckoutProducts',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('checkout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mainapp.checkout')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mainapp.product')),
            ],
        ),
    ]
