from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


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
    donator = models.ManyToManyField('Donator',
                                     verbose_name=_('donator'),
                                     null=True,
                                     blank=True)

    def __unicode__(self):
        return self.name

    def get_donators(self):
        return ", ".join([dn.name for dn in self.donator.all()])
    get_donators.short_description = _('donator')

    class Meta:
        ordering = ['-donate_date']
        verbose_name = _('book')
        verbose_name_plural = _('book')


class Donator(models.Model):
    name = models.CharField(max_length=250, verbose_name=_("donator name"))
    description = models.TextField(blank=True,
                                   null=True,
                                   verbose_name=_("description"))
    contact_info = models.TextField(blank=True,
                                    null=True,
                                    verbose_name=_("contact info"))

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("detail_donator", kwargs={'pk': self.id})

    class Meta:
        verbose_name = _('donator')
        verbose_name_plural = _('donator')
