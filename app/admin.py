from django.contrib import admin
from .models import *

admin.site.register([UserType,Items,Table,TableBill,Item_Sale,Access,Month,Year,MonthMatch])

# Register your models here.
