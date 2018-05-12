from django.db import models

# Create your models here.
class Property(models.Model):
    address = models.CharField(max_length=200, unique=True)
    house_img = models.URLField(max_length=200)
    loc_rating = models.DecimalField(decimal_places=1)
    fac_rating = models.DecimalField(decimal_places=1)
    tran_rating = models.DecimalField(decimal_places=1)
    comment=models.CharField(max_length=20, blank=True)
    no_bed = models.IntegerField(max_length=20, blank=True)
    no_bath = models.IntegerField(max_length=20, blank=True)

    def __str__(self):
        return self.address



class Agency(models.Model):
    name = models.CharField(max_length=30)
    agent_img = models.URLField(max_length=200)
    company = models.CharField(max_length=20, blank=True)
    comany_logo = models.URLField(max_length=200)
    fri_rating = models.DecimalField(decimal_places=1)
    res_rating = models.DecimalField(decimal_places=1)
    bond_rating = models.DecimalField(decimal_places=1)
    comment=models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name

class Resource(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    link = models.URLField(max_length=200)
    price = models.IntegerField(max_length=20)

