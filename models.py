from django.db import models


class Donator(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True)

    def __unicode__(self):
        return self.name


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
