# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import SmartResize
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from urllib import quote


class Book(models.Model):
    STATUS = (
        (0, _('store up')),
        (1, _('circulate')),
        (2, _('unknow')),
    )
    name = models.CharField(max_length=250, verbose_name=_('book name'))
    author_name = models.CharField(max_length=250,
                                   null=True,
                                   blank=True,
                                   verbose_name=_('author'))
    amount = models.IntegerField(verbose_name=_('amount'))
    donate_date = models.DateField(verbose_name=_('donate date'))
    publisher = models.CharField(max_length=120,
                                 null=True,
                                 blank=True,
                                 verbose_name=_('publisher'))
    publish_date = models.DateField(null=True,
                                    blank=True,
                                    verbose_name=_('publish date'))
    status = models.IntegerField(max_length=25,
                                 choices=STATUS,
                                 default=0,
                                 verbose_name=_('status'))
    description = models.TextField(blank=True,
                                   null=True,
                                   verbose_name=_("description"))
    donor = models.ManyToManyField('Donor',
                                   verbose_name=_('donor'),
                                   null=True,
                                   blank=True)
    photos = generic.GenericRelation('Photo',
                                     content_type_field='content_type',
                                     object_id_field='object_id')

    def __unicode__(self):
        return self.name

    def get_donors(self):
        return ", ".join([dn.name for dn in self.donor.all()])
    get_donors.short_description = _('donor')

    def get_absolute_url(self):
        return reverse("detail_book", kwargs={'pk': self.id})

    def get_search_url(self):
        url = ("http://202.192.155.48:83/opac/searchresult.aspx?"
               "ANYWORDS=%s&dt=ALL&cl=ALL&dp=20"
               "&sf=M_PUB_YEAR&ob=DESC&sm=table&dept=ALL")
        url = (url % quote(self.name.encode("GBK")))

        return url

    def get_cover(self):
        if (0 < self.photos.count()):
            return self.photos.all()[0]

        return

    class Meta:
        ordering = ['-donate_date']
        verbose_name = _('book')
        verbose_name_plural = _('books')


class Donor(models.Model):
    TYPE = (
        (0, _('personal')),
        (1, _('organization')),
    )
    name = models.CharField(max_length=250, verbose_name=_("donor name"))
    description = models.TextField(blank=True,
                                   null=True,
                                   verbose_name=_("description"))
    donor_type = models.IntegerField(max_length=25,
                                     choices=TYPE,
                                     default=1,
                                     verbose_name=_('donor type'))
    contact_info = models.TextField(blank=True,
                                    null=True,
                                    verbose_name=_("contact info"))

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("detail_donor", kwargs={'pk': self.id})

    def get_books_string(self):
        string = ""

        for bk in self.book_set.all():
            string += u"《" + bk.name + u"》，"
            if (52 < len(string)):
                break

        if (1 < len(string)):
            string = string[:-1]

        if (52 < len(string)):
            string += u"……"

        return string

    def get_cover(self):
        if (0 < self.book_set.count()):
            for bk in self.book_set.all():
                cover = bk.get_cover
                if (cover):
                    return cover

        return

    class Meta:
        verbose_name = _('donor')
        verbose_name_plural = _('donors')


class Photo(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('photo name'))
    image = models.ImageField(upload_to='zenshu_book_photo',
                              verbose_name=_('Image'))
    thumbnail = ImageSpecField(image_field='image',
                               processors=[SmartResize(75, 100)],
                               format='JPEG',
                               options={'quality': 60})
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('photo')
        verbose_name_plural = _('photos')
