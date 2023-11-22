# Create your views here.
from django.shortcuts import  render, redirect
from .forms import *
from django.contrib.auth import login, authenticate,logout #add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #add this
from django.db.models import Count, Sum, Avg, Max, Min
from django.db.models import F, ExpressionWrapper
from datetime import date
from app.models import *
import datetime
from django.utils import timezone
from datetime import timedelta


def home(request):
    return render(request,"app/base.html")


def homepage(request):
	return render (request=request, template_name="app/header.html")
	

def register_request(request):
	print(request.POST)
	if request.method == "POST":
		form = NewUserForm(request.POST)
		print(form)
		print("1")
		if form.is_valid():
			print("2")
			user = form.save()
			login(request, user)
			print("3")
			messages.success(request, "Registration successful." )
			return redirect("/login")
		messages.error(request, "Unsuccessful registration. Invalid information.")
		print("4")
	form = NewUserForm()
	return render (request=request, template_name="app/register.html", context={"register_form":form})
def bash_view(request):
    return render(request, 'app/header.html')

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("main:homepage")

def login_request(request):

	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				print("id",user.id)
				user_type = Access.objects.get(user_map = user.id).user_type_map
				print(type(user_type.name))

				if user_type.name=="server":
					tables = Table.objects.all()
					return render(request,'app/table.html',context={"tables":tables,"user_id":user.id})
				if user_type.name=="master":
					order = Item_Sale.objects.filter(bill=False,kitchen=False)
					return render(request,'app/kitchen.html',{'list':order})
				if user_type.name=="cashier":
					row = Table.objects.all()
					return render(request,"app/billing.html",{"tables":row,'date':datetime.datetime.now().date()})

				if user_type.name=="owner":
					
					return render(request,"app/owner_view.html",{"user_id":user.id})

				#type of login
				return redirect("/home")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="app/login.html", context={"login_form":form})


def order_place(request,table_id,user_id):
	print(request.POST)
	form = Item_Sale_form() 
	if request.method == 'POST':
		print(request.POST.get('submitted') == '1')
		item = Items.objects.get(id=request.POST["item_name"])
		print(item)
		print(type(item.price))
		prices = int(item.price)
		form = Item_Sale_form(request.POST)
		print(prices)
		print(type(prices))
		print(type(item))
		print("tab",Table.objects.get(id=int(table_id)).table_no)
		print("na",User.objects.get(id=int(user_id)).first_name)

		itemsale = Item_Sale(
			table_no = Table.objects.get(id=int(table_id)),
			user = User.objects.get(id=int(user_id)),
			item_name = item,
			count = request.POST["count"],
			total_price = int(request.POST["count"]) * prices
		)
		print(itemsale.id)
		if request.POST.get('submitted') == '1':
			itemsale.save()
		order = Item_Sale.objects.filter(bill=False,table_no=Table.objects.get(id=int(table_id)))
			#return redirect('home')
		tables = Table.objects.all()
		return render(request,'app/table.html',context={"tables":tables,"user_id":user_id,"form":form,"order":order})
    
	tables = Table.objects.all()
	order = Item_Sale.objects.filter(bill=False,table_no=Table.objects.get(id=int(table_id)))
	return render(request,'app/table.html',context={"tables":tables,"user_id":user_id,"form":form,"order":order})


def kitchen_view(request,id=0):
	if id == 0:
		order = Item_Sale.objects.filter(bill=False,kitchen=False)
		print("hai")
		print(len(order))
		return render(request,'app/kitchen.html',{'list':order})
	else:
		order = Item_Sale.objects.get(id=int(id))
		order.kitchen = True
		print("bye")
		order.save()
		order = Item_Sale.objects.filter(bill=False,kitchen=False)
		return render(request,'app/kitchen.html',{'list':order})


def bill_counter(request,id=0):
	if id ==0:
		row = Table.objects.all()
		return render(request,"app/billing.html",{"tables":row,'date':datetime.datetime.now().date()})

	if Item_Sale.objects.filter(table_no = int(id),bill = False).exists():
		bill = Item_Sale.objects.filter(table_no = int(id),bill = False)
		list =[]
		
		sum = 0
		items = []
		for i in bill:
			dic2={}
			if i.bill == False:
				table = i.table_no
				print(i.pk)
				user=i.user
				ids =Item_Sale.objects.get(id=i.pk)
				items.append(ids)
				dic2['name']=i.item_name
				dic2['count']=i.count
				dic2["price"]=i.item_name.price
				price = dic2['total_price']=i.total_price
				sum+=int(price)
			list.append(dic2)
			tablebill = TableBill(table_no = table, total_price = sum,user=user)
			tablebill.save()
			tables = Table.objects.all()
		return render(request,'app/billing.html',{'tables':tables,'list':list,'date':datetime.datetime.now().date(),'grand_total':sum,'table':table.table_no})
	else :
		tables = Table.objects.all()
		return redirect('/billcounter/0')
	
def billstatus(request,id):
    items = Item_Sale.objects.filter(table_no = id)
    for i in items:
        i.bill=True
        i.save()
    return redirect('/billcounter/0')



def table(request):
	item = Items.objects.filter(is_active=True).values_list('name',flat=True)
	print(item)
	tables = Table.objects.all()
	return render(request,'app/table.html',context={"items":item , "tables":tables})

def owner_view(request):
	return render(request,"app/owner_view.html")

def daily_report(request):
	date = datetime.datetime.now().date()
	sale = Item_Sale.objects.filter(date__date=date)
	print(date)
	print(len(sale))
	amount = sale.aggregate(total=Sum('total_price'))["total"]
	print(amount)
	return render(request,"app/today_report.html",context={"name":"DAILY SALE","items":sale,"date":date,"amount":amount})


# def billcounter(request,id=0):

def monthly_report(request):
	# Get today's date
	form = Month_Year()
	print(request.POST)
	if request.method == 'POST':
		print("")
		list =[]
		month = int(request.POST["month"])
		print("month",type(month),month)
		year = Year.objects.get(id = int(request.POST["year"][0])).year
		print("year",type(year),year)
		
		sale = Item_Sale.objects.filter(date__month=month,date__year=year)
		print(len(sale))
		amount = sale.aggregate(total=Sum('total_price'))["total"]
		item = Items.objects.all().values_list('name',flat=True)
		print(item)
		print(amount)
		print("yes")
		for items in item:
			dic = {} 
			dic["name"] = items
			dic["total_price"] = sale.filter(item_name__name = items).aggregate(total=Sum('total_price'))["total"]
			dic["count"] = sale.filter(item_name__name = items).aggregate(total=Sum('count'))["total"]
			print(items)
			print(dic)
			list.append(dic)

		date = str(month) +"/"+ str(year)
		return render(request,"app/monthly_report.html",context={"name":"MONTHLY SALE","list":list,"date":date,"amount":amount,"form":form})

	print("no")
	return render(request,"app/monthly_report.html",context={"name":"MONTHLY SALE","form":form})

def daywise(request):
	form = DateForm()
	print(request.POST)
	if request.method == 'POST':
		date = request.POST['date']
		list = []
		sale = Item_Sale.objects.filter(date__date=date)
		if sale.exists():

			print(len(sale))
			amount = sale.aggregate(total=Sum('total_price'))["total"]
			item = Items.objects.all().values_list('name',flat=True)
			print(item)
			print(amount)
			print("yes")
			for items in item:
				dic = {} 
				dic["name"] = items
				dic["total_price"] = sale.filter(item_name__name = items).aggregate(total=Sum('total_price'))["total"]
				dic["count"] = sale.filter(item_name__name = items).aggregate(total=Sum('count'))["total"]
				print(items)
				print(dic)
				list.append(dic)

			
			return render(request,"app/monthly_report.html",context={"name":"MONTHLY SALE","list":list,"date":date,"amount":amount,"form":form})

	print("no")
	return render(request,"app/monthly_report.html",context={"name":"MONTHLY SALE","form":form})




