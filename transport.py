from django.db import models
from zenshu.models import Book, Donator
from django.utils.encoding import smart_str
from django.db.models import Sum


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


def pre_trans():
#    presents = ZshPresent.objects.all().order_by('id')
#    for pt in presents:
#        pt.present_name = pt.present_name.strip()
#        if pt.info is not None:
#            pt.info = pt.info.strip()
#        if pt.contact2 is not None:
#            pt.contact2 = pt.contact2.strip()
#        pt.save()
#        print(pt.id)

    zbks = ZshBook.objects.all().order_by('id')
    for zbk in zbks:
        zbk.bookname = zbk.bookname.strip()
        if zbk.present_name is not None:
            zbk.present_name = zbk.present_name.strip()
#        if zbk.publisher is not None:
#            zbk.publisher = zbk.publisher.strip()
#        if zbk.author is not None:
#            zbk.author = zbk.author.strip()
#        if zbk.info is not None:
#            zbk.info = zbk.info.strip()
        zbk.save()
        print(zbk.id)


def trans():
    presents = ZshPresent.objects.all()

    for pt in presents:
        pt_name = pt.present_name
        dns = Donator.objects.filter(name=pt_name)
        if (0 == dns.count()):
            dn = Donator()
            dn.name = pt_name
            if pt.info is not None:
                dn.description = pt.info
            if pt.contact2 is not None:
                dn.contact_info = pt.contact2
            dn.save()

            zshbooks = ZshBook.objects.filter(
                present_name=pt_name)

            for zbk in zshbooks:
                bk = Book()
                bk.name = zbk.bookname
                if pt.sent_time is not None:
                    bk.donate_date = pt.sent_time
                else:
                    bk.donate_date = '1990-02-28'
                if zbk.vols:
                    bk.amount = zbk.vols
                else:
                    bk.amount = 1
                if zbk.author is not None:
                    bk.author_name = zbk.author
                if zbk.info is not None:
                    bk.description = zbk.info
                if zbk.publisher is not None:
                    bk.publisher = zbk.publisher
                if zbk.info is not None:
                    bk.description = zbk.info
                bk.publish_date = zbk.public_date
                bk.save()
                bk.donator.add(dn)
                bk.save()
                print bk.id
        else:
            print("%d, %s" % (pt.id, smart_str(pt_name)))


def trans2():
    zshbooks = ZshBook.objects.all()

    for zbk in zshbooks:
        dns = Donator.objects.filter(name=zbk.present_name)
        if (0 == dns.count()):
            print("%d %s\n" % (zbk.id, smart_str(zbk.bookname)))
            dn = Donator()
            dn.name = zbk.present_name
            dn.save()
            bk = Book()

            all_book_with_this_present = ZshBook.objects.filter(
                present_name=zbk.present_name)

            for zshbook in all_book_with_this_present:
                bk = Book()
                bk.name = zshbook.bookname
                bk.donate_date = '1990-02-28'
                if zshbook.vols:
                    bk.amount = zbk.vols
                else:
                    bk.amount = 1
                if zshbook.author is not None:
                    bk.author_name = zshbook.author
                if zshbook.info is not None:
                    bk.description = zshbook.info
                if zshbook.publisher is not None:
                    bk.publisher = zshbook.publisher
                bk.publish_date = zshbook.public_date
                bk.save()
                bk.donator.add(dn)
                bk.save()
                print(bk.id)


def check():
    zshbooks = ZshBook.objects.all()

    for zbk in zshbooks:
        bks = Book.objects.filter(name=zbk.bookname.strip())

        if (0 == bks.count()):
            print("%d %s\n" % (zbk.id, smart_str(zbk.bookname)))


def check2():
    pass


def check3():
    dns = Donator.objects.all()
    for dn in dns:
        total = dn.book_set.count()
        print total
