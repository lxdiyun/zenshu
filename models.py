from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class Donator(models.Model):
    name = models.CharField(max_length=250, verbose_name=_("donator name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("description"))

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("detail_donator", kwargs={'pk':self.id})

    class Meta:
        verbose_name = _('donator')
        verbose_name_plural = _('donator')


class Book(models.Model):
    name = models.CharField(max_length=250)
    donator = models.ManyToManyField(Donator)
    author_name = models.CharField(max_length=250)
    amount = models.IntegerField()
    donate_date = models.DateField('Donate Date')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['donate_date']
