# Generated by Django 2.2.10 on 2021-09-08 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(null=True)),
                ('ticker', models.TextField(max_length=5)),
                ('market_capitalization', models.IntegerField()),
                ('dividend', models.BooleanField()),
            ],
            options={
                'ordering': ['ticker'],
            },
        ),
        migrations.CreateModel(
            name='StockPriceGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(null=True)),
                ('type', models.TextField(null=True)),
                ('stock_ids', models.ManyToManyField(to='orders.StockInfo')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='StockPriceByDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('regular_price', models.IntegerField()),
                ('min_price', models.IntegerField()),
                ('max_price', models.IntegerField()),
                ('group_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='group_id', to='orders.StockPriceGroup')),
                ('ticket_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stock_info_id', to='orders.StockInfo')),
            ],
        ),
    ]
