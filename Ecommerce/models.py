from django.db import models

# Create your models here.

class Productmetadata(models.Model):
    asin = models.CharField(primary_key=True, max_length=255)
    salesrank = models.TextField(db_column='salesRank', blank=True, null=True)  # Field name made lowercase.
    imurl = models.TextField(db_column='imUrl', blank=True, null=True)  # Field name made lowercase.
    categories = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    related = models.TextField(blank=True, null=True)
    brand = models.TextField(blank=True, null=True)
    also_bought = models.TextField(blank=True, null=True)
    also_viewed = models.TextField(blank=True, null=True)
    bought_together = models.TextField(blank=True, null=True)
    buy_after_viewing = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ProductMetadata'


class Asintocategory(models.Model):
    record_id = models.IntegerField(primary_key=True)  # The composite primary key (record_id, asin) found, that is not supported. The first column is selected.
    asin = models.CharField(max_length=255)
    category_level_1 = models.CharField(db_column='Category_Level_1', max_length=255, blank=True, null=True)  # Field name made lowercase.
    category_level_2 = models.CharField(db_column='Category_Level_2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    category_level_3 = models.CharField(db_column='Category_Level_3', max_length=255, blank=True, null=True)  # Field name made lowercase.
    category_level_4 = models.CharField(db_column='Category_Level_4', max_length=255, blank=True, null=True)  # Field name made lowercase.
    category_level_5 = models.CharField(db_column='Category_Level_5', max_length=255, blank=True, null=True)  # Field name made lowercase.
    category_level_6 = models.CharField(db_column='Category_Level_6', max_length=255, blank=True, null=True)  # Field name made lowercase.
    category_level_7 = models.CharField(db_column='Category_Level_7', max_length=255, blank=True, null=True)  # Field name made lowercase.
    category_level_8 = models.CharField(db_column='Category_Level_8', max_length=255, blank=True, null=True)  # Field name made lowercase.
    category_level_9 = models.CharField(db_column='Category_Level_9', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'asintocategory'
        unique_together = (('record_id', 'asin'),)



class Asintosalesrank(models.Model):
    asin = models.CharField(primary_key=True, max_length=255)  # The composite primary key (asin, category) found, that is not supported. The first column is selected.
    category = models.CharField(max_length=255)
    sales_rank = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'asintosalesrank'
        unique_together = (('asin', 'category'),)



class Asintosimplecategory(models.Model):
    record_id = models.IntegerField(primary_key=True)  # The composite primary key (record_id, asin) found, that is not supported. The first column is selected.
    asin = models.CharField(max_length=255)
    category = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'asintosimplecategory'
        unique_together = (('record_id', 'asin'),)

class Reviwes(models.Model):
    reviewerid = models.CharField(db_column='reviewerID', max_length=255)  # Field name made lowercase.
    asin = models.CharField(primary_key=True, max_length=255)  # The composite primary key (asin, reviewerID) found, that is not supported. The first column is selected.
    reviewername = models.TextField(db_column='reviewerName', blank=True, null=True)  # Field name made lowercase.
    helpful = models.TextField(blank=True, null=True)
    reviewtext = models.TextField(db_column='reviewText', blank=True, null=True)  # Field name made lowercase.
    overall = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    reviewtime = models.DateField(db_column='reviewTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'reviwes'
        unique_together = (('asin', 'reviewerid'),)
