# Generated by Django 4.1.5 on 2024-08-05 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p1App', '0008_remove_paymentmodel_amount_paymentmodel_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='investeddb',
            name='amount_invested',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='investeddb',
            name='date_invested',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
