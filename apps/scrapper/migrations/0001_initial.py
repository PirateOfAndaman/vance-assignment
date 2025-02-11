# Generated by Django 5.0.7 on 2024-07-26 15:10

import common.helpers
import django.core.serializers.json
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('meta', models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True)),
                ('code', models.CharField(max_length=3, unique=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', common.helpers.BaseManager()),
            ],
        ),
        migrations.CreateModel(
            name='CurrencyExchange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('meta', models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True)),
                ('from_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exchanges_from', to='scrapper.currency')),
                ('to_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exchanges_to', to='scrapper.currency')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', common.helpers.BaseManager()),
            ],
        ),
    ]
