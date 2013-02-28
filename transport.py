from django.db import models
from zenshu.models import Book, Donator
from django.utils.encoding import smart_str


class ZshBook(models.Model):
    id = models.IntegerField()
    bookname = models.CharField(max_length=60)
    author = models.CharField(max_length=60, blank=True)
    publisher = models.CharField(max_length=60, blank=True)
    public_date = models.CharField(max_length=10, blank=True)
    vols = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=10)
    present_name = models.CharField(max_length=60)
    info = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = u'zsh_book'


class ZshPresent(models.Model):
    id = models.IntegerField()
    present_name = models.CharField(max_length=60)
    sent_time = models.DateTimeField(null=True, blank=True)
    vols = models.IntegerField()
    contact = models.CharField(max_length=100, blank=True)
    info = models.CharField(max_length=200, blank=True)
    contact2 = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = u'zsh_present'


def trans():
    presents = ZshPresent.objects.all()

    for pt in presents:
        dn = Donator()
        dn.name = pt.present_name.strip()
        if pt.info is not None:
            dn.description = pt.info.strip()
        if pt.contact2 is not None:
            dn.contact_info = pt.contact2.strip()
        dn.save()

        zshbooks = ZshBook.objects.filter(present_name=pt.present_name)

        for zbk in zshbooks:
            bk = Book()
            bk.name = zbk.bookname.strip()
            if pt.sent_time is not None:
                bk.donate_date = pt.sent_time
            else:
                bk.donate_date = '1990-02-28'
            if zbk.vols:
                bk.amount = zbk.vols
            else:
                bk.amount = 1
            if zbk.author is not None:
                bk.author_name = zbk.author.strip()
            if zbk.info is not None:
                bk.description = zbk.info.strip()
            if zbk.publisher is not None:
                bk.publisher = zbk.publisher.strip()
            bk.publish_date = zbk.public_date
            bk.save()
            bk.donator.add(dn)
            bk.save()
            print bk.id


def trans2():
    zshbooks = ZshBook.objects.all()

    for zbk in zshbooks:
        dns = Donator.objects.filter(name=zbk.present_name.strip())
        if (0 == dns.count()):
            print("%d %s\n", zbk.id, smart_str(zbk.bookname))
            bk = Book()
            bk.name = zbk.bookname.strip()
            bk.donate_date = '1990-02-28'
            if zbk.vols:
                bk.amount = zbk.vols
            else:
                bk.amount = 1
            if zbk.author is not None:
                bk.author_name = zbk.author.strip()
            if zbk.info is not None:
                bk.description = zbk.info.strip()
            if zbk.publisher is not None:
                bk.publisher = zbk.publisher.strip()
            bk.publish_date = zbk.public_date
            bk.save()

            dn = Donator()
            dn.name = zbk.present_name.strip()
            dn.save()
            dn.book_set.add(bk)
            dn.save()
