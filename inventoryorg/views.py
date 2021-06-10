from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login

from .models import *
from .forms import *
from django.http import JsonResponse

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

# from rest_framework.views import APIView
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from django.core import serializers
# from django.conf import Settings
# from django.http import Http404
# import json

import csv
from dateutil import relativedelta
from datetime import datetime, date

# Create your views here.

#-----------------------------Admin Account-------------------------------#


def adminac(request, value=0, pk='0'):
    if request.user.is_anonymous or pk == 'logoutuser' or request.user.acc_type != 'AD':
        return redirect('/login/')

    elif request.user.acc_type == 'AD':

        queryset1 = Account.objects.all()
        queryset2 = Employee.objects.all()
        queryset3 = Product.objects.all()
        queryset4 = Productlist.objects.all()
        queryset5 = Invt_mgt.objects.all()
        arr = [0, 0, 0, 0]
        arr[0] = queryset2.count()
        arr[1] = Productlist.objects.filter(status='AV').count()
        arr[2] = Productlist.objects.filter(status='IS').count()
        arr[3] = Employee.objects.values('department').distinct().count()
        form1 = AccountCreateform(request.POST or None)
        form2 = Employeeform(request.POST or None)
        form3 = Productform(request.POST or None)
        form4 = Productlistform(request.POST or None)
        form5 = Invt_mgtform(request.POST or None)
        form6 = Invt_mgtIssueform(request.POST or None)
        form7 = AccountUpdateform(request.POST or None)
        form8 = EmployeeUpdateform(request.POST or None)
        form9 = Invt_mgtReturnform(request.POST or None)
        form10 = DownloadReport(request.POST or None)
        context = {
            'form1': form1,
            'form2': form2,
            'form3': form3,
            'form4': form4,
            'form5': form5,
            'form6': form6,
            'form10': form10,
            'arr': arr,
            'queryset1': queryset1,
            'queryset2': queryset2,
            'queryset3': queryset3,
            'queryset4': queryset4,
            'queryset5': queryset5,
        }
        if request.method == 'POST' and value == 1:
            if form1.is_valid():
                form1.save()
                return redirect('adminac', value=0)
            # else:
            #     return redirect('adminac', value=1)

        if request.method == 'POST' and value == 3:
            try:
                if form2.is_valid:
                    form2.save()
                    return redirect('adminac', value=2)
            except:
                return redirect('adminac', value=3)
            # else:
            #     return redirect('adminac', value=3)

        if request.method == 'POST' and value == 6:
            if form6.is_valid():
                instance = form6.save(commit=False)
                pk = str(instance.product_id).split(':')
                pk = pk[0].rstrip()
                queryset3 = Product.objects.get(product_id=pk)
                queryset3.quantity -= 1
                queryset4 = Productlist.objects.get(
                    product_serial=instance.product_serial)
                queryset4.status = 'IS'
                now = datetime.now()
                hr = int(now.strftime('%H'))
                mn = int(now.strftime('%M'))
                sn = int(now.strftime('%S'))
                instance.issue_date = instance.issue_date.replace(
                    hour=hr, minute=mn, second=sn)
                queryset3.save()
                queryset4.save()
                instance.save()
                return redirect('adminac', value=7)
            # else:
            #     return redirect('adminac', value=6)

        if value == 0 and pk == '0':
            return render(request, 'admin0.html', context)
        if value == 0 and pk != '0':
            queryset1 = Account.objects.get(username=pk)
            form7 = AccountUpdateform(instance=queryset1)
            if request.method == 'POST':
                form7 = AccountUpdateform(request.POST, instance=queryset1)
                if form7.is_valid():
                    form7.save()
                    return redirect('adminac', value=0)
                # else:
                #     return HttpResponse('Invalid value entered while updating Account!')
            context = {
                'queryset1': queryset1,
                'form7': form7,
            }
            return render(request, 'admin00.html', context)
        if value == 1:
            return render(request, 'admin1.html', context)
        if value == 2 and pk == '0':
            return render(request, 'admin2.html', context)
        if value == 22 and pk != '0':
            queryset2 = Employee.objects.get(employee_id=pk)
            form8 = EmployeeUpdateform(instance=queryset2)
            if request.method == 'POST':
                form8 = EmployeeUpdateform(request.POST, instance=queryset2)
                if form8.is_valid():
                    form8.save()
                    return redirect('adminac', value=2, pk='0')
            context = {
                'queryset2': queryset2,
                'form8': form8,
                'arr': arr,
            }
            return render(request, 'admin22.html', context)
        if value == 3:
            return render(request, 'admin3.html', context)
        if value == 4:
            return render(request, 'admin4.html', context)
        if value == 5 and pk == '0':
            temp = request.user.id
            try:
                queryset2 = Employee.objects.get(email=temp)
                temp = str(queryset2.employee_id).split(':')
                temp = temp[0].rstrip()
                queryset5 = Invt_mgt.objects.filter(employee_id=temp)
                queryset5 = queryset5.filter(reporting_date=None)
                queryset5 = queryset5.exclude(return_date=None)
                context = {
                    'queryset5': queryset5,
                    'arr': arr,
                }
                return render(request, 'admin5.html', context)
            except:
                return redirect('adminac',value=3)

        if value == 55 and pk != '0':
            queryset5 = Invt_mgt.objects.get(id=pk)
            form9 = Invt_mgtReturnform(instance=queryset5)
            if request.method == 'POST':
                form9 = Invt_mgtReturnform(request.POST, instance=queryset5)
                if form9.is_valid():
                    temp = form9.save(commit=False)
                    if temp.reporting_date != None:
                        queryset4 = Productlist.objects.get(
                            product_serial=temp.product_serial)
                        queryset4.status = 'AV'
                        pk = str(queryset4.product_id).split(':')
                        pk = pk[0].rstrip()
                        queryset3 = Product.objects.get(product_id=pk)
                        if len(temp.remark) == 0:
                            queryset3.quantity += 1
                        now = datetime.now()
                        hr = int(now.strftime('%H'))
                        mn = int(now.strftime('%M'))
                        sn = int(now.strftime('%S'))
                        temp.reporting_date = temp.reporting_date.replace(
                            hour=hr, minute=mn, second=sn)
                        queryset3.save()
                        queryset4.save()
                    if len(temp.remark) != 0:
                        queryset4 = Productlist.objects.get(
                            product_serial=temp.product_serial)
                        queryset4.status = 'UM'
                        queryset4.save()
                    temp.save()
                    return redirect('adminac', value=5, pk='0')
                else:
                    return HttpResponse('Invalid value entered while Returning Item!')
            context = {
                'queryset5': queryset5,
                'form9': form9,
                'arr': arr,
            }
            return render(request, 'admin55.html', context)

        if value == 6:
            return render(request, 'admin6.html', context)
        if value == 7:
            if request.method == 'POST':
                if form10['export_to_csv'].value() == True:
                    response = HttpResponse(content_type='text/csv')
                    response['Content-Disposition'] = 'attachment; filename="Transactions.csv"'
                    writer = csv.writer(response)
                    writer.writerow(['Transaction_id', 'Employee_Id:Name', 'Product_Id:Name',
                                    'Product_serial', 'Issue_date', 'Return_date', 'Reporting_date', 'Remark'])
                    instance = queryset5
                    for t in instance:
                        writer.writerow([t.pk, t.employee_id, t.product_id,
                                         t.product_serial, t.issue_date, t.return_date, t.reporting_date, t.remark])
                    return response
            return render(request, 'admin7.html', context)
        if value == 99:
            try:
                temp = request.user.id
                queryset1 = Account.objects.get(id=temp)
                queryset2 = Employee.objects.get(email=temp)
                form1 = AccountUpdateform1(instance=queryset1)
                form2 = EmployeeUpdateform(instance=queryset2)
                if request.method == 'POST':
                    form1 = AccountUpdateform1(
                        request.POST or None, instance=queryset1)
                    form2 = EmployeeUpdateform(
                        request.POST or None, instance=queryset2)
                    if form1.is_valid():
                        form1.save()
                    if form2.is_valid():
                        form2.save()
                    return redirect('adminac', value=99)
                context = {
                    'form1': form1,
                    'form2': form2,
                    'arr': arr,
                }
                return render(request, 'admin99.html', context)
            except:
                return redirect('adminac',value=3)
        if value == 100:
            if request.method == 'POST':
                form = PasswordChangeForm(request.user, request.POST)
                if form.is_valid():
                    user = form.save()
                    update_session_auth_hash(request, user)
                    return redirect('adminac', value=99)
                else:
                    return redirect('adminac', value=100)
            form = PasswordChangeForm(request.user)
            context = {
                'form': form,
                'arr': arr,
            }
            return render(request, 'admin100.html', context)

#----------------------------Manager Account------------------------------#


def managerac(request, value=0, pk='0'):

    if request.user.is_anonymous or pk == 'logoutuser' or request.user.acc_type != 'MG':
        return redirect('/logoutuser')

    elif request.user.acc_type == 'MG':
        queryset3 = Product.objects.all()
        queryset4 = Productlist.objects.all()
        queryset5 = Invt_mgt.objects.all()
        arr = [0, 0, 0, 0]
        arr[0] = queryset4.count()
        arr[1] = Productlist.objects.filter(status='AV').count()
        arr[2] = Productlist.objects.filter(status='IS').count()
        arr[3] = Productlist.objects.filter(status='UM').count()
        form3 = Productform(request.POST or None)
        form4 = Productlistform(request.POST or None)
        form7 = AccountUpdateform(request.POST or None)
        form8 = EmployeeUpdateform(request.POST or None)
        form9 = Invt_mgtReturnform(request.POST or None)
        form10 = ProductUpdateform(request.POST or None)
        context = {
            'form3': form3,
            'form4': form4,
            'form7': form7,
            'form8': form8,
            'form9': form9,
            'form10': form10,
            'arr': arr,
            'queryset3': queryset3,
            'queryset4': queryset4,
            'queryset5': queryset5,
        }

        if value == 0 and pk == '0':
            return render(request, 'manager0.html', context)
        if value == 0 and pk != '0':
            queryset3 = Product.objects.get(product_id=pk)
            form10 = ProductUpdateform(instance=queryset3)
            if request.method == 'POST':
                form10 = ProductUpdateform(request.POST, instance=queryset3)
                if form10.is_valid():
                    form10.save()
                return redirect('managerac', value=0, pk='0')
            context = {
                'queryset3': queryset3,
                'form10': form10,
                'arr': arr,
            }
            return render(request, 'manager00.html', context)
        if value == 1:
            if request.method == 'POST':
                if form3.is_valid():
                    form3.save()
                    return redirect('managerac', value=0)
            return render(request, 'manager1.html', context)
        if value == 2 and pk == '0':
            return render(request, 'manager2.html', context)
        if value == 3 and pk == '0':
            if request.method == 'POST':
                if form4.is_valid():
                    form4.save()
                    return redirect('managerac', value=2)
            return render(request, 'manager3.html', context)
        if (value == 21 or value == 22 or value == 23) and pk != '0':
            queryset4 = Productlist.objects.get(product_serial=pk)
            temp = str(queryset4.product_id).split(':')
            temp = temp[0].rstrip()
            queryset3 = Product.objects.get(product_id=temp)
            if value == 21:
                if queryset4.status != 'AV':
                    queryset4.status = 'AV'
                    queryset3.quantity += 1
            if value == 22:
                if queryset4.status != 'UM':
                    queryset4.status = 'UM'
                    queryset3.quantity -= 1
            if value == 23:
                if queryset4.status != 'IS':
                    queryset4.status = 'IS'
                    queryset3.quantity -= 1
            queryset3.save()
            queryset4.save()
            return redirect('managerac', value=2)
        if value == 4 and pk == '0':
            return render(request, 'manager4.html', context)
        if value == 44 and pk != '0':
            form11 = ProductIssueform(request.POST or None, pk=pk)
            if request.method == 'POST':
                queryset1 = Account.objects.get(username=request.user.username)
                queryset2 = Employee.objects.get(email=queryset1.id)
                queryset3 = Product.objects.get(product_id=pk)
                queryset3.quantity -= 1
                queryset3.save()
                print('Queryset Quantity : ', queryset3.quantity)
                temp = form11.save(commit=False)
                queryset4 = Productlist.objects.get(
                    product_serial=temp.product_serial)
                queryset4.status = 'IS'
                queryset4.save()
                print('Queryset Status : ', queryset4.status)
                temp.employee_id = queryset2
                temp.product_id = queryset3
                now = datetime.now()
                hr = int(now.strftime('%H'))
                mn = int(now.strftime('%M'))
                sn = int(now.strftime('%S'))
                temp.issue_date = temp.issue_date.replace(
                    hour=hr, minute=mn, second=sn)
                if queryset3.is_returnable == True:
                    today = date.today() + relativedelta.relativedelta(months=1)
                    d2 = today.strftime('%Y-%m-%d')
                    temp.return_date = d2
                temp.save()
                return redirect('managerac', value=5)
            context = {
                'form11': form11,
                'arr': arr,
            }
            return render(request, 'manager44.html', context)
        if value == 5 and pk == '0':
            try:
                temp = request.user.id
                queryset2 = Employee.objects.get(email=temp)
                temp = str(queryset2.employee_id).split(':')
                temp = temp[0].rstrip()
                queryset5 = Invt_mgt.objects.filter(employee_id=temp)
                queryset5 = queryset5.filter(reporting_date=None)
                queryset5 = queryset5.exclude(return_date=None)
                context = {
                    'queryset5': queryset5,
                    'arr': arr,
                }
                return render(request, 'manager5.html', context)
            except:
                return redirect('managerac',value=4)
        if value == 55 and pk != '0':
            queryset5 = Invt_mgt.objects.get(id=pk)
            form9 = Invt_mgtReturnform(instance=queryset5)
            if request.method == 'POST':
                form9 = Invt_mgtReturnform(request.POST, instance=queryset5)
                if form9.is_valid():
                    temp = form9.save(commit=False)
                    if temp.reporting_date != None:
                        queryset4 = Productlist.objects.get(
                            product_serial=temp.product_serial)
                        queryset4.status = 'AV'
                        pk = str(queryset4.product_id).split(':')
                        pk = pk[0].rstrip()
                        queryset3 = Product.objects.get(product_id=pk)
                        if len(temp.remark) == 0:
                            queryset3.quantity += 1
                        now = datetime.now()
                        hr = int(now.strftime('%H'))
                        mn = int(now.strftime('%M'))
                        sn = int(now.strftime('%S'))
                        temp.reporting_date = temp.reporting_date.replace(
                            hour=hr, minute=mn, second=sn)
                        queryset3.save()
                        queryset4.save()
                    if len(temp.remark) != 0:
                        queryset4 = Productlist.objects.get(
                            product_serial=temp.product_serial)
                        queryset4.status = 'UM'
                        queryset4.save()
                    temp.save()
                    return redirect('managerac', value=5)
                # else:
                #     return HttpResponse('Invalid value entered while Returning Item!')
            context = {
                'queryset5': queryset5,
                'form9': form9,
                'arr': arr,
            }
            return render(request, 'manager55.html', context)
        if value == 6:
            return render(request, 'manager6.html', context)
        if value == 99:
            try:
                temp = request.user.id
                queryset1 = Account.objects.get(id=temp)
                queryset2 = Employee.objects.get(email=temp)
                form1 = AccountUpdateform1(instance=queryset1)
                form2 = EmployeeUpdateform(instance=queryset2)
                if request.method == 'POST':
                    form1 = AccountUpdateform1(
                        request.POST or None, instance=queryset1)
                    form2 = EmployeeUpdateform(
                        request.POST or None, instance=queryset2)
                    if form1.is_valid():
                        form1.save()
                    if form2.is_valid():
                        form2.save()
                    return redirect('managerac', value=99)
                context = {
                    'form1': form1,
                    'form2': form2,
                    'arr': arr,
                }
                return render(request, 'manager99.html', context)
            except:
                return redirect('managerac',value=6)
        if value == 100:
            if request.method == 'POST':
                form = PasswordChangeForm(request.user, request.POST)
                if form.is_valid():
                    user = form.save()
                    update_session_auth_hash(request, user)
                    return redirect('managerac', value=99)
                else:
                    return redirect('managerac', value=100)
            form = PasswordChangeForm(request.user)
            context = {
                'form': form,
                'arr': arr,
            }
            return render(request, 'manager100.html', context)

# -----------------------------Staff Account------------------------------#


def staffac(request, value=0, pk='0'):

    if request.user.is_anonymous or pk == 'logoutuser' or request.user.acc_type != 'ST':
        return redirect('/login')

    elif request.user.acc_type == 'ST':
        queryset3 = Product.objects.all()
        queryset4 = Productlist.objects.all()
        queryset5 = Invt_mgt.objects.all()
        arr = [0, 0, 0, 0]
        # arr[0] = queryset4.count()
        # arr[1] = Productlist.objects.filter(status='AV').count()
        temp = request.user.id
        queryset2 = Employee.objects.get(email=temp)
        temp = str(queryset2.employee_id).split(':')
        temp = temp[0].rstrip()
        queryset5 = Invt_mgt.objects.filter(employee_id=temp)
        arr[3] = queryset5.count()
        queryset5 = queryset5.filter(reporting_date=None)
        queryset5 = queryset5.exclude(return_date=None)
        arr[2] = queryset5.count()
        form3 = Productform(request.POST or None)
        form9 = Invt_mgtReturnform(request.POST or None)
        context = {
            'form3': form3,
            'form9': form9,
            'arr': arr,
            'queryset3': queryset3,
            'queryset5': queryset5,
        }

        if value == 0 and pk == '0':
            return render(request, 'staff0.html', context)
        if value == 0 and pk != '0':
            form11 = ProductIssueform(request.POST or None, pk=pk)
            if request.method == 'POST':
                queryset1 = Account.objects.get(username=request.user.username)
                queryset2 = Employee.objects.get(email=queryset1.id)
                queryset3 = Product.objects.get(product_id=pk)
                queryset3.quantity -= 1
                queryset3.save()
                temp = form11.save(commit=False)
                queryset4 = Productlist.objects.get(
                    product_serial=temp.product_serial)
                queryset4.status = 'IS'
                queryset4.save()
                temp.employee_id = queryset2
                temp.product_id = queryset3
                if queryset3.is_returnable == True:
                    today = date.today() + relativedelta.relativedelta(months=1)
                    d2 = today.strftime('%Y-%m-%d')
                    temp.return_date = d2
                now = datetime.now()
                hr = int(now.strftime('%H'))
                mn = int(now.strftime('%M'))
                sn = int(now.strftime('%S'))
                temp.issue_date = temp.issue_date.replace(
                    hour=hr, minute=mn, second=sn)
                temp.save()
                return redirect('staffac', value=1)
            context = {
                'form11': form11,
                'arr': arr,
            }
            return render(request, 'staff00.html', context)
        if value == 1 and pk == '0':
            try:
                temp = request.user.id
                queryset2 = Employee.objects.get(email=temp)
                temp = str(queryset2.employee_id).split(':')
                temp = temp[0].rstrip()
                queryset5 = Invt_mgt.objects.filter(employee_id=temp)
                queryset5 = queryset5.filter(reporting_date=None)
                queryset5 = queryset5.exclude(return_date=None)
                context = {
                    'queryset5': queryset5,
                    'arr': arr,
                }
                return render(request, 'staff1.html', context)
            except:
                return redirect('staffac',value=0)
        if value == 11 and pk != '0':
            queryset5 = Invt_mgt.objects.get(id=pk)
            form9 = Invt_mgtReturnform(instance=queryset5)
            if request.method == 'POST':
                form9 = Invt_mgtReturnform(request.POST, instance=queryset5)
                if form9.is_valid():
                    temp = form9.save(commit=False)
                    if temp.reporting_date != None:
                        queryset4 = Productlist.objects.get(
                            product_serial=temp.product_serial)
                        queryset4.status = 'AV'
                        pk = str(queryset4.product_id).split(':')
                        pk = pk[0].rstrip()
                        queryset3 = Product.objects.get(product_id=pk)
                        if len(temp.remark) == 0:
                            queryset3.quantity += 1
                        now = datetime.now()
                        hr = int(now.strftime('%H'))
                        mn = int(now.strftime('%M'))
                        sn = int(now.strftime('%S'))
                        temp.reporting_date = temp.reporting_date.replace(
                            hour=hr, minute=mn, second=sn)
                        queryset3.save()
                        queryset4.save()
                    if len(temp.remark) != 0:
                        queryset4 = Productlist.objects.get(
                            product_serial=temp.product_serial)
                        queryset4.status = 'UM'
                        queryset4.save()
                    temp.save()
                    return redirect('staffac', value=0)
                # else:
                #     return HttpResponse('Invalid value entered while Returning Item!')
            context = {
                'queryset5': queryset5,
                'form9': form9,
                'arr': arr,
            }
            return render(request, 'staff11.html', context)
        if value == 2:
            try:
                temp = request.user.id
                queryset2 = Employee.objects.get(email=temp)
                temp = str(queryset2.employee_id).split(':')
                temp = temp[0].rstrip()
                queryset5 = Invt_mgt.objects.filter(employee_id=temp)
                context = {
                    'queryset5': queryset5,
                    'arr': arr,
                }
                return render(request, 'staff2.html', context)
            except:
                return redirect('staffac',value=0)
        if value == 99:
            try:
                temp = request.user.id
                queryset1 = Account.objects.get(id=temp)
                queryset2 = Employee.objects.get(email=temp)
                form1 = AccountUpdateform1(instance=queryset1)
                form2 = EmployeeUpdateform(instance=queryset2)
                if request.method == 'POST':
                    form1 = AccountUpdateform1(
                        request.POST or None, instance=queryset1)
                    form2 = EmployeeUpdateform(
                        request.POST or None, instance=queryset2)
                    if form1.is_valid():
                        form1.save()
                    if form2.is_valid():
                        form2.save()
                    return redirect('staffac', value=99)
                context = {
                    'form1': form1,
                    'form2': form2,
                    'arr': arr,
                }
                return render(request, 'staff99.html', context)
            except:
                return redirect('staffac',value=0)
        if value == 100:
            if request.method == 'POST':
                form = PasswordChangeForm(request.user, request.POST)
                if form.is_valid():
                    user = form.save()
                    update_session_auth_hash(request, user)
                    return redirect('staffac', value=99)
                else :
                    return redirect('staffac', value=100)
            form = PasswordChangeForm(request.user)
            context = {
                'form': form,
                'arr': arr,
            }
            return render(request, 'staff100.html', context)

#--------------------------------Login/Logout----------------------------#

def loginuser(request):
    error1 = {
        'error1': "*Invalid Username or Password"
    }
    error2 = {
        'error2': "*Incorrect Account Type"
    }
    error3 = {
        'error3': "*Select Account Type"
    }
    if request.method == "POST":
        usrname = request.POST.get('username')
        passwd = request.POST.get('password')
        acc_type = request.POST.get('acc_type')

        user = authenticate(username=usrname, password=passwd)

        if user is not None and acc_type != 'Account Type':

            if user.acc_type == 'AD' and user.acc_type == acc_type:
                login(request, user)
                return redirect("adminac", value=0)

            if user.acc_type == 'MG' and user.acc_type == acc_type:
                login(request, user)
                return redirect("managerac", value=0)

            if user.acc_type == 'ST' and user.acc_type == acc_type:
                login(request, user)
                return redirect("staffac", value=0)

            if user.acc_type != acc_type:
                return render(request, 'Login.html', error2)

        else:

            if acc_type == 'Account Type':
                return render(request, 'Login.html', error3)

            else:
                return render(request, 'Login.html', error1)

    return render(request, 'Login.html')


def logoutuser(request, **kwargs):
    logout(request)
    return redirect('/login')

# ---------------------------------ajax--------------------------------- #


def load_serial(request):
    product_id = request.GET.get('product_id')
    serials = Productlist.objects.filter(product_id=product_id, status='AV')
    return JsonResponse(list(serials.values('product_serial')), safe=False)
