# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import adli.utils


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250, verbose_name='book name')),
                ('author_name', models.CharField(max_length=250, null=True, verbose_name='author', blank=True)),
                ('amount', models.IntegerField(verbose_name='amount')),
                ('donate_date', models.DateField(verbose_name='donate date')),
                ('publisher', models.CharField(max_length=120, null=True, verbose_name='publisher', blank=True)),
                ('publish_date', models.DateField(null=True, verbose_name='publish date', blank=True)),
                ('status', models.IntegerField(default=0, verbose_name='status', choices=[(0, 'store up'), (1, 'circulate'), (2, 'unknow')])),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
            ],
            options={
                'ordering': ['-donate_date'],
                'verbose_name': 'book',
                'verbose_name_plural': 'books',
            },
        ),
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250, verbose_name='donor name')),
                ('name_index', models.CharField(max_length=2)),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('donor_type', models.IntegerField(default=1, verbose_name='donor type', choices=[(0, 'personal'), (1, 'organization')])),
                ('contact_info', models.TextField(null=True, verbose_name='contact info', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'donor',
                'verbose_name_plural': 'donors',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250, verbose_name='photo name')),
                ('image', models.ImageField(upload_to=adli.utils.random_path_and_rename('zengshu_book_photo'), verbose_name='Image')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'photo',
                'verbose_name_plural': 'photos',
            },
        ),
        migrations.CreateModel(
            name='ZshBook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_1', models.IntegerField()),
                ('bookname', models.CharField(max_length=60)),
                ('author', models.CharField(max_length=60, blank=True)),
                ('publisher', models.CharField(max_length=60, blank=True)),
                ('public_date', models.CharField(max_length=10, blank=True)),
                ('vols', models.IntegerField(null=True, blank=True)),
                ('status', models.CharField(max_length=10)),
                ('present_name', models.CharField(max_length=60)),
                ('info', models.CharField(max_length=200, blank=True)),
            ],
            options={
                'db_table': 'zsh_book',
            },
        ),
        migrations.CreateModel(
            name='ZshPresent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_1', models.IntegerField()),
                ('present_name', models.CharField(max_length=60)),
                ('sent_time', models.DateTimeField(null=True, blank=True)),
                ('vols', models.IntegerField()),
                ('contact', models.CharField(max_length=100, blank=True)),
                ('info', models.CharField(max_length=200, blank=True)),
                ('contact2', models.CharField(max_length=200, blank=True)),
            ],
            options={
                'db_table': 'zsh_present',
            },
        ),
        migrations.AddField(
            model_name='book',
            name='donor',
            field=models.ManyToManyField(to='zengshu.Donor', verbose_name='donor', blank=True),
        ),
    ]
