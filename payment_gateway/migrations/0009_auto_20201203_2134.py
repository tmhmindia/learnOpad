# Generated by Django 3.1.4 on 2020-12-03 16:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment_gateway', '0008_auto_20201203_1826'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='razorpaydetails',
            name='order',
        ),
        migrations.AddField(
            model_name='order',
            name='razorpay',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payment_gateway.razorpaydetails'),
        ),
        migrations.CreateModel(
            name='FacilitatorSubscriptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(blank=True, choices=[('1', '4999'), ('2', '7499'), ('3', '9999')], max_length=250, null=True)),
                ('status', models.BooleanField(default=False)),
                ('razorpay', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payment_gateway.razorpaydetails')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
