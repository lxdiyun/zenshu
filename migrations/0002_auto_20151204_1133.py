# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('zengshu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250, verbose_name='batch name')),
                ('date', models.DateField(verbose_name='date')),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': 'batch',
                'verbose_name_plural': 'batches',
            },
        ),
        migrations.CreateModel(
            name='BookStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250, verbose_name='book status name')),
            ],
            options={
                'verbose_name': 'book status',
                'verbose_name_plural': 'book status',
            },
        ),
        migrations.CreateModel(
            name='BookType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250, verbose_name='book type name')),
            ],
            options={
                'verbose_name': 'book type',
                'verbose_name_plural': 'book types',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='log time')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
            ],
            options={
                'ordering': ['-time'],
                'verbose_name': 'log',
                'verbose_name_plural': 'logs',
            },
        ),
        migrations.AlterModelOptions(
            name='donor',
            options={'verbose_name': 'donor', 'verbose_name_plural': 'donors'},
        ),
        migrations.AddField(
            model_name='book',
            name='collected_amount',
            field=models.IntegerField(null=True, verbose_name='collected amount', blank=True),
        ),
        migrations.AddField(
            model_name='book',
            name='control_number',
            field=models.IntegerField(null=True, verbose_name='control number', blank=True),
        ),
        migrations.AddField(
            model_name='book',
            name='last_modify_by',
            field=models.ForeignKey(default=1, verbose_name='last modify by', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='last_modify_date',
            field=models.DateField(auto_now_add=True, verbose_name='last modify date', null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='status',
            field=models.ForeignKey(default=1, verbose_name='status', to='zengshu.BookStatus'),
        ),
        migrations.AddField(
            model_name='log',
            name='book',
            field=models.ForeignKey(to='zengshu.Book'),
        ),
        migrations.AddField(
            model_name='log',
            name='operator',
            field=models.ForeignKey(verbose_name='operator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='book',
            name='batch',
            field=models.ForeignKey(verbose_name='batch', blank=True, to='zengshu.Batch', null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='book_type',
            field=models.ForeignKey(default=1, verbose_name='book type', to='zengshu.BookType'),
            preserve_default=False,
        ),
    ]
