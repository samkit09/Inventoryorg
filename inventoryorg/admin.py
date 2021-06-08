from django.contrib import admin
from .models import *
from .forms import *

# Register your models here.


class Accountadmin(admin.ModelAdmin):
    list_display = ['username', 'email',
                    'acc_type','is_admin','is_active']
    form = AccountCreateform
    list_filter = ['acc_type']
    search_fields = ['username', 'email']


class Employeeadmin(admin.ModelAdmin):
    list_display = ['employee_id', 'employee_name',
                    'email', 'contact', 'department']
    form = Employeeform
    list_filter = ['department']
    search_fields = ['employee_id', 'employee_name', 'email', 'contact']


class Productadmin(admin.ModelAdmin):
    list_display = ['product_id', 'product_name',
                    'category', 'brand', 'price', 'quantity', 'vendor']
    form = Productform
    list_filter = ['category', 'brand', 'is_returnable']
    search_fields = ['product_id', 'product_name',
                     'vendor', 'price', 'quantity']

class Productlistadmin(admin.ModelAdmin):
    list_display = ['product_serial', 'product_id','status']
    form = Productlistform
    list_filter = ['product_id','status']
    search_fields = ['product_id']


class Invt_mgtadmin(admin.ModelAdmin):
    list_display = ['pk', 'employee_id',
                    'product_id', 'product_serial', 'issue_date', 'return_date', 'reporting_date', 'remark']
    form = Invt_mgtform
    list_filter = ['product_id', 'employee_id']
    search_fields = ['transaction_id', 'employee_id',
                     'product_id', 'product_serial', 'issue_date', 'return_date', 'reporting_date', 'remark']


admin.site.register(Account, Accountadmin)
admin.site.register(Employee, Employeeadmin)
admin.site.register(Product, Productadmin)
admin.site.register(Productlist, Productlistadmin)
admin.site.register(Invt_mgt, Invt_mgtadmin)
