# -*- coding: utf-8 -*-
from django.db import models
from models import Book, Donor
from django.utils.encoding import smart_str, smart_text
#from django.db.models import Sum


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
    presents = ZshPresent.objects.all().order_by('id')
    for pt in presents:
        pt.present_name = pt.present_name.strip()
        if pt.info is not None:
            pt.info = pt.info.strip()
        if pt.contact2 is not None:
            pt.contact2 = pt.contact2.strip()
        pt.save()
        print(pt.id)

    zbks = ZshBook.objects.all().order_by('id')
    for zbk in zbks:
        zbk.bookname = zbk.bookname.strip()
        if zbk.present_name is not None:
            zbk.present_name = zbk.present_name.strip()
        if zbk.publisher is not None:
            zbk.publisher = zbk.publisher.strip()
        if zbk.author is not None:
            zbk.author = zbk.author.strip()
        if zbk.info is not None:
            zbk.info = zbk.info.strip()
        zbk.save()
        print(zbk.id)


def trans_book(dn, pt):
    zshbooks = ZshBook.objects.filter(present_name=pt.present_name)

    for zbk in zshbooks:
        bk = Book()
        bk.name = zbk.bookname
        if (pt.sent_time is not None) and ("" != pt.sent_time):
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
        bk.save()
        bk.donor.add(dn)
        bk.save()
        print(bk.id)


def trans_dn(pt, dn_name):
    dn = Donor()
    dn.name = dn_name
    if (3 >= pt.length):
        dn.donor_type = 0
    if pt.info is not None:
        dn.description = pt.info
    if pt.contact2 is not None:
        dn.contact_info = pt.contact2
    dn.save()

    return dn


def trans():
    presents = ZshPresent.objects.extra(
        select={'length': 'Length(present_name)'})

    for pt in presents:
        pt_name = pt.present_name
#        print(smart_str(pt_name))
        pt_name_exists = Donor.objects.filter(name=pt_name).exists()

        if (pt_name_exists):
            dn_name = pt_name + smart_text("(0)")
            trans_dn(pt, dn_name)
        else:
            dn_name = pt_name
            dn = trans_dn(pt, dn_name)
            trans_book(dn, pt)


def trans2():
    zshbooks = ZshBook.objects.extra(
        select={'length': 'Length(present_name)'})

    for zbk in zshbooks:
        pt_name_exists = Donor.objects.filter(name=zbk.present_name).exists()
        if (not pt_name_exists):
            print("%d %s\n" % (zbk.id, smart_str(zbk.bookname)))
            dn = Donor()
            dn.name = zbk.present_name
            if (3 >= zbk.length):
                dn.donor_type = 0
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
#                bk.publish_date = zshbook.public_date
                bk.save()
                bk.donor.add(dn)
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
    dns = Donor.objects.all()
    for dn in dns:
        total = dn.book_set.count()
        print total

g_merge_dict = {}


def make_merge_list():
    dns = Donor.objects.all()

    for dn in dns:
        if ('' != dn.name):
            name = dn.name.replace(")", u"）").replace("(", u"（")
            same_name_dns = Donor.objects.filter(
                name__regex="^\d?"+name+smart_text(
                    "[(（\d）)]*$")).order_by('id')
            try:
                if (1 < same_name_dns.count()):
                    merge_list = []

                    for sdn in same_name_dns:
                        if (dn.id != sdn.id):
                            merge_list.append(sdn.id)
                    g_merge_dict[dn.id] = merge_list
            finally:
                print(smart_str(dn.name))

    for key in g_merge_dict.keys():
        key_name = Donor.objects.get(id=key).name
        dn_ids = g_merge_dict[key]
        dn_names = Donor.objects.filter(id__in=dn_ids).values_list('name',
                                                                   flat=True)
        dn_names_smart = map(smart_str, dn_names)
        print("%s:[%s]" % (smart_str(key_name), "".join(dn_names_smart)))


def merge_dn(key_dn, dn):
    if dn.contact_info is not None:
        if key_dn.contact_info is not None:
            key_dn.contact_info += "\n" + dn.contact_info
        else:
            key_dn.contact_info = dn.contact_info
    if dn.description is not None:
        if key_dn.description is not None:
            key_dn.description += "\n" + dn.description
        else:
            key_dn.description = dn.description

    key_dn.book_set.add(*dn.book_set.values_list('id', flat=True))


def merge():
    for key in g_merge_dict.keys():
        key_dn = Donor.objects.get(id=key)
        print key_dn
        dn_ids = g_merge_dict[key]
        dns = Donor.objects.filter(id__in=dn_ids)
        for dn in dns:
            merge_dn(key_dn, dn)
        key_dn.save()

    for dn_ids in g_merge_dict.values():
        Donor.objects.filter(id__in=dn_ids).all().delete()
