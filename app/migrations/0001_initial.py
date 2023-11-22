# Generated by Django 4.2.6 on 2023-10-08 11:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('price', models.IntegerField()),
                ('is_active', models.BooleanField(default=False)),
                ('created_by', models.DateTimeField(auto_now_add=True)),
                ('modified_by', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_no', models.PositiveIntegerField()),
                ('created_by', models.DateTimeField(auto_now_add=True)),
                ('modified_by', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('created_by', models.DateTimeField(auto_now_add=True)),
                ('modified_by', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TableBill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('total_price', models.IntegerField()),
                ('items', models.IntegerField(blank=True, null=True)),
                ('table_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.table')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item_Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=50)),
                ('count', models.PositiveIntegerField()),
                ('kitchen', models.BooleanField(default=False)),
                ('total_price', models.PositiveIntegerField(blank=True)),
                ('bill', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now=True)),
                ('table_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.table')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
