from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class Book(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('book name'))
    author_name = models.CharField(max_length=250, verbose_name=_('author'))
    amount = models.IntegerField(verbose_name=_('amount'))
    donate_date = models.DateField(verbose_name=_('donate date'))
    donator = models.ManyToManyField('Donator',
                                     verbose_name=_('donator'),
                                     null=True,
                                     blank=True)

    def __unicode__(self):
        return "%s/%s/%d" % (self.name, self.author_name, self.amount)

    class Meta:
        ordering = ['donate_date']
        verbose_name = _('book')
        verbose_name_plural = _('book')


class Donator(models.Model):
    name = models.CharField(max_length=250, verbose_name=_("donator name"))
    description = models.TextField(blank=True,
                                   null=True,
                                   verbose_name=_("description"))

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("detail_donator", kwargs={'pk': self.id})

    class Meta:
        verbose_name = _('donator')
        verbose_name_plural = _('donator')
