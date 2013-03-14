from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import SmartResize


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

    def __unicode__(self):
        return self.name

    def get_donors(self):
        return ", ".join([dn.name for dn in self.donor.all()])
    get_donors.short_description = _('donor')

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

    class Meta:
        verbose_name = _('donor')
        verbose_name_plural = _('donors')


class Photo(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('photo name'))
    image = models.ImageField(upload_to='zenshu_book_photo',
                              verbose_name=_('Image'))
    thumbnail = ImageSpecField(image_field='image',
                               processors=[SmartResize(100, 50)],
                               format='JPEG',
                               options={'quality': 60})
    book = models.ForeignKey('Book',
                             verbose_name=(_('book')),
                             null=True,
                             blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('photo')
        verbose_name_plural = _('photos')
