from django.urls import path,include
from app import views

app_name = "app" 
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
    path('bash/', views.bash_view, name='bash_view'),
    path('table/', views.table, name='table'),
    path("home",views.home,name="home"),
    path("order/<int:table_id>/<int:user_id>",views.order_place,name="order"),
    path('kitchen/<int:id>/',views.kitchen_view,name="kitchen"),
    path("billcounter/<int:id>/",views.bill_counter,name="billcounter"),
    path('billstatus/<int:id>',views.billstatus,name='billstatus'),
    path('owner',views.owner_view,name="owner_view"),
    path('dailyreport',views.daily_report,name='dailyreport'),
    path('monthlyreport',views.monthly_report,name="monthlyreport"),
    path('daywise',views.daywise,name="daywise"),

]
