from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

#--------------dependency class--------------#


class DateInput(forms.DateInput):
    input_type = 'date'

#----------------------Main Forms--------------------------#


class Accountform(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'email', 'acc_type',
                  'password', 'is_admin', 'is_active']


class AccountCreateform(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Account
        fields = UserCreationForm.Meta.fields + \
            ('email', 'acc_type', 'is_admin', 'is_active')


class Employeeform(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_id', 'employee_name',
                  'email', 'contact', 'department']


class Productform(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_id', 'product_name', 'category',
                  'brand', 'quantity', 'vendor', 'price', 'is_returnable']


class Productlistform(forms.ModelForm):
    class Meta:
        model = Productlist
        fields = ['product_id', 'product_serial', 'status']


class Invt_mgtform(forms.ModelForm):
    class Meta:
        model = Invt_mgt
        fields = ['employee_id',
                  'product_id', 'product_serial', 'issue_date', 'return_date', 'reporting_date', 'remark']
#----------------------Return Forms--------------------------#


class Invt_mgtReturnform(forms.ModelForm):
    class Meta:
        model = Invt_mgt
        fields = ['reporting_date', 'remark']
        widgets = {
            'reporting_date': DateInput(),
        }

#----------------------Update Forms--------------------------#


class AccountUpdateform(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'email', 'acc_type', 'is_admin', 'is_active']


class AccountUpdateform1(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'email']


class EmployeeUpdateform(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_name', 'contact', 'department']


class ProductUpdateform(forms.ModelForm):
    class Meta():
        model = Product
        fields = ['product_name', 'category', 'brand',
                  'price', 'quantity', 'vendor', 'is_returnable']

#----------------------Custom Forms--------------------------#


class Invt_mgtIssueform(forms.ModelForm):
    class Meta:
        model = Invt_mgt
        fields = ['employee_id',
                  'product_id', 'product_serial', 'issue_date', 'return_date']
        widgets = {
            'issue_date': DateInput(),
            'return_date': DateInput(),
        }
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['product_serial'].queryset = Productlist.objects.none()


class ProductIssueform(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('pk')
        super().__init__(*args, **kwargs)
        self.fields['product_serial'].queryset = Productlist.objects.filter(
            status='AV', product_id=pk)

    class Meta:
        model = Invt_mgt
        fields = ['product_serial', 'issue_date']
        widgets = {
            'issue_date': DateInput(),
        }


class DownloadReport(forms.ModelForm):
    export_to_csv = forms.BooleanField(required=False)
    class Meta:
        model= Invt_mgt
        fields = []
