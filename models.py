# -*- coding: utf-8 -*-
import re

from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.auth.models import User as Operator

from imagekit.models import ImageSpecField
from imagekit.processors import SmartResize

import pinyin

from adli.utils import random_path_and_rename


class BookType(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('book type name'))

    class Meta:
        verbose_name = _('book type')
        verbose_name_plural = _('book types')

    def __str__(self):
        return self.name


class Log(models.Model):
    time = models.DateTimeField(auto_now_add=True, verbose_name=_('log time'))
    description = models.TextField(blank=True, null=True, verbose_name=_("log content"))
    operator = models.ForeignKey(Operator, verbose_name=_('operator'), on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-time']
        verbose_name = _('log')
        verbose_name_plural = _('logs')

    def __str__(self):
        return "%s|%s|%s" % (self.time.strftime("%Y-%m-%d"),
                             self.operator,
                             self.description)


class Batch(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('batch name'))
    date = models.DateField(verbose_name=_('date'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date']
        verbose_name = _('batch')
        verbose_name_plural = _('batches')


class BookStatus(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('book status name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('book status')
        verbose_name_plural = _('book status')


class Book(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('book name'))
    book_type = models.ForeignKey(BookType, verbose_name=_('book type'), on_delete=models.CASCADE)
    donate_date = models.DateField(verbose_name=_('donate date'))
    amount = models.IntegerField(verbose_name=_('amount'))
    collected_amount = models.IntegerField(null=True, blank=True, verbose_name=_('collected amount'))
    control_number = models.IntegerField(null=True, blank=True, verbose_name=_('control number'))
    batch = models.ForeignKey(Batch, blank=True, null=True,
                              verbose_name=_("batch"), on_delete=models.CASCADE)
    author_name = models.CharField(max_length=250, null=True, blank=True, verbose_name=_('author'))
    publisher = models.CharField(max_length=120, null=True, blank=True, verbose_name=_('publisher'))
    publish_date = models.DateField(null=True, blank=True, verbose_name=_('publish date'))
    status = models.ForeignKey(BookStatus, verbose_name=_("status"), default=1, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True, verbose_name=_("description"))
    donor = models.ManyToManyField('Donor', verbose_name=_('donor'), blank=True)
    last_modify_date = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name=_('last modify date'))
    last_modify_by = models.ForeignKey(Operator, verbose_name=_('last modify by'), on_delete=models.CASCADE)
    photos = GenericRelation('Photo', content_type_field='content_type', object_id_field='object_id')

    class Meta:
        ordering = ['-donate_date']
        verbose_name = _('book')
        verbose_name_plural = _('books')

    def __str__(self):
        return self.name

    def get_donors(self):
        return ", ".join([dn.name for dn in self.donor.all()])
    get_donors.short_description = _('donor')

    def get_absolute_url(self):
        return reverse("zengshu:detail_book", kwargs={'pk': self.id})

    def get_search_url(self):
        url = "http://202.192.155.48:83/opac/search.aspx"
        if self.control_number:
            url = "http://202.192.155.48:83/opac/bookinfo.aspx?ctrlno=%d"
            url = (url % self.control_number)

        return url

    def get_cover(self):
        if (0 < self.photos.count()):
            return self.photos.all()[0]

        return

    def get_recent_logs(self):
        string = ""
        for log in self.log_set.all()[:5]:
            string += "#%s\n <br> \n" % (log)

        return string
    get_recent_logs.short_description = _('recent logs')
    get_recent_logs.allow_tags = True


class Donor(models.Model):
    TYPE = (
        (0, _('personal')),
        (1, _('organization')),
    )
    name = models.CharField(max_length=250, verbose_name=_("donor name"))
    name_index = models.CharField(max_length=2)
    description = models.TextField(blank=True, null=True, verbose_name=_("description"))
    donor_type = models.IntegerField(choices=TYPE, default=1, verbose_name=_('donor type'))
    contact_info = models.TextField(blank=True, null=True, verbose_name=_("contact info"))

    class Meta:
        verbose_name = _('donor')
        verbose_name_plural = _('donors')

    def save(self, *args, **kwargs):
        name_pinyin = re.sub("[^a-zA-z ]", "", pinyin.get_initial(self.name, ""))
        self.name_index = name_pinyin[:1].upper()
        super(Donor, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("zengshu:detail_donor", kwargs={'pk': self.id})


class Photo(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('photo name'))
    image = models.ImageField(upload_to=random_path_and_rename('zengshu_book_photo'), verbose_name=_('Image'))
    thumbnail = ImageSpecField(source='image',
                               processors=[SmartResize(75, 100)],
                               format='JPEG',
                               options={'quality': 60})
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('photo')
        verbose_name_plural = _('photos')
