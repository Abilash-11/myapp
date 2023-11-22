from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserType(models.Model):
    name = models.CharField(max_length=30)
    created_by = models.DateTimeField(auto_now_add=True)
    modified_by = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Items(models.Model):
    name = models.CharField(max_length=30)
    price = models.IntegerField()
    is_active = models.BooleanField(default=False)
    created_by = models.DateTimeField(auto_now_add=True)
    modified_by = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Table(models.Model):
    table_no = models.PositiveIntegerField()
    created_by = models.DateTimeField(auto_now_add=True)
    modified_by = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

class TableBill(models.Model):
    table_no = models.ForeignKey(Table,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    total_price = models.IntegerField()
    items = models.ManyToManyField('Item_Sale', blank=True)
    #items = my_list = models.ManyToManyField(Item_Sale,null=True)

class Item_Sale(models.Model):
    table_no = models.ForeignKey(Table,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    item_name = models.ForeignKey(Items,on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
    kitchen = models.BooleanField(default=False)
    total_price = models.PositiveIntegerField(blank=True)
    bill = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.item_name

class Access(models.Model):
    user_map = models.ForeignKey(User,on_delete=models.CASCADE)
    user_type_map = models.ForeignKey(UserType,on_delete=models.CASCADE)

class Month(models.Model):
    month = models.CharField(max_length=20)

    def __str__(self):
        return self.month


class Year(models.Model):
    year = models.IntegerField()

    def __str__(self):
        return str(self.year)

class MonthMatch(models.Model):
    month = models.ForeignKey(Month,on_delete=models.CASCADE)
    year = models.ForeignKey(Year,on_delete=models.CASCADE)