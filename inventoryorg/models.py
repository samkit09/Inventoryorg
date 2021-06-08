import django.db.models as m
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
# from django.conf import settings
# from django.contrib.auth import get_user_model
# from django.db.models.deletion import SET
# from django.forms import ModelForm, Textarea
# Create your models here.


def get_def():
    val = 'DELETED'
    return val
    # return get_user_model().objects.get_or_create(username='Deleted')[0]


def get_defm():
    val = 'DELETED@mail.com'
    return val


class AccountManager(BaseUserManager):
    def create_user(self, username, email, acc_type, password=None):
        if not email:
            raise ValueError('Users must have an email address!')
        if not username:
            raise ValueError('Users must have an username!')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            acc_type=acc_type,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, acc_type, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            acc_type=acc_type,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    acc_types = (
        ('AD', 'Admin'),
        ('MG', 'Manager'),
        ('ST', 'Staff'),
    )
    email = m.EmailField(verbose_name='Email',
                         max_length=255, unique=True)
    username = m.CharField(verbose_name='Username', max_length=30, unique=True)
    date_joined = m.DateTimeField(
        verbose_name='Date_Joined', auto_now_add=True)
    last_login = m.DateTimeField(verbose_name='Last_Login', auto_now_add=True)
    is_admin = m.BooleanField(default=False)
    is_active = m.BooleanField(default=True)
    is_staff = m.BooleanField(default=False)
    is_superuser = m.BooleanField(default=False)
    acc_type = m.CharField(verbose_name='Account_Type',
                           max_length=2, choices=acc_types, default='ST',help_text='(AD,MG,ST)')
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'acc_type']

    objects = AccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Employee(m.Model):
    employee_id = m.CharField(verbose_name='Employee ID',
                              max_length=11, primary_key=True)
    employee_name = m.CharField(
        verbose_name='Employee Name', max_length=255)
    email = m.OneToOneField('Account', on_delete=m.PROTECT)
    contact = PhoneNumberField(verbose_name='Contact Number')
    department = m.CharField(verbose_name='Department',
                             max_length=30)

    def __str__(self):
        return self.employee_id+' : '+self.employee_name

    class Meta():
        db_table = "Iemployee"


class Product(m.Model):
    product_id = m.CharField(verbose_name="Product ID",
                             max_length=10, primary_key=True)
    product_name = m.CharField(
        max_length=40)
    category = m.CharField(verbose_name="Category", max_length=40)
    brand = m.CharField(verbose_name="Brand",
                        max_length=40, default='Unbranded')
    price = m.DecimalField(verbose_name="Price",
                           max_digits=8, decimal_places=2, default=0)
    vendor = m.CharField(verbose_name="Vendor Name",
                         max_length=50, default='Unknown')
    quantity = m.PositiveIntegerField(verbose_name="Quantity", default=0)
    is_returnable = m.BooleanField(verbose_name="Is Returnable", default=True)

    def __str__(self):
        return self.product_id+' : '+self.product_name

    class Meta():
        db_table = "Iproduct"


class Productlist(m.Model):
    status_type = (
        ('AV', 'Available'),
        ('UM', 'Under_Maintenance'),
        ('IS', 'Issued'),
    )
    product_serial = m.CharField(
        verbose_name="Product Serial Number", max_length=10, primary_key=True)
    product_id = m.ForeignKey('Product', on_delete=m.PROTECT)
    status = m.CharField(verbose_name='Status',
                         max_length=2, choices=status_type, default='AV',help_text='(AV, UM, IS)')

    def __str__(self):
        return self.product_serial

    class Meta():
        db_table = "Iproductlist"


class Invt_mgt(m.Model):
    transaction_id = m.AutoField(
        verbose_name="Transaction_id", primary_key=True),
    employee_id = m.ForeignKey('Employee', on_delete=m.CASCADE)
    product_id = m.ForeignKey('Product', on_delete=m.DO_NOTHING)
    product_serial = m.ForeignKey('Productlist', on_delete=m.DO_NOTHING)
    issue_date = m.DateTimeField(
        verbose_name="Issued On", auto_now_add=False, auto_now=False, editable=True)
    return_date = m.DateTimeField(
        verbose_name="Return On", auto_now_add=False, auto_now=False, blank=True, null=True, editable=True)
    reporting_date = m.DateTimeField(
        verbose_name="Reported On", auto_now_add=False, auto_now=False, blank=True, null=True, editable=True)
    remark = m.TextField(verbose_name="Remarks",
                         blank=True, null=True, default=None)
    

    def __str__(self):
        return (str(self.pk))

    class Meta():
        db_table = "Iinvt_mgt"
