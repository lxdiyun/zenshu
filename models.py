from django.db import models
from django.core.urlresolvers import reverse


class Donator(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        print self.id
        return reverse("detail_donator", kwargs={'pk':self.id})


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
