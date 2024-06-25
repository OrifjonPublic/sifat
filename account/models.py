from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_delete


# Asosiy korxona modeli
class Company(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    # telegram_url = models.URLField()

    def __str__(self):
        return self.name    


def fake_user():
    user, created = User.objects.get_or_create(
        username='+998123456789',
        defaults={
            'first_name': 'Deleted',
            'last_name': 'Account'
        }
    )
    return user


class Role(models.Model):
    name = models.CharField(max_length=255)


# Custom user manager
class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The username field must be set')
        user = self.model(user=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

# Custom user model
class User(AbstractBaseUser, PermissionsMixin):
    DIRECTOR = 'director'
    ASSISTANT = 'admin'
    DEPARTMENT_HEAD = 'manager'
    EMPLOYEE = 'xodim'
    
    ROLE_CHOICES = [
        (DIRECTOR, 'Director'),
        (ASSISTANT, 'Admin'),
        (DEPARTMENT_HEAD, 'Manager'),
        (EMPLOYEE, 'Xodim'),
    ]
    GENDER = [
        ('male', 'Erkak'),
        ('female', 'Ayol')
    ]
    gender = models.CharField(max_length=10, choices=GENDER, default='male')
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='user_department')
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='1.png', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


# Mahsulot modeli
class Product(models.Model):
    unique_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    production_time = models.DurationField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

# Bolim modeli
class Department(models.Model):
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.head:
            self.head = fake_user()
        super().save(*args, **kwargs)

    def set_user_(self, *args, **kwargs):
        self.head = fake_user()
        super().save(*args, **kwargs)


# Nuqson modeli
class Defect(models.Model):
    unique_id = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

# Ish faoliyati modeli (bolim boshligi tomonidan kiritiladi)
class WorkRecord(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    work_time = models.DurationField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='work_records_created', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.employee} - {self.product} - {self.quantity}'


@receiver(pre_delete, sender=User)
def set_default_created_by(sender, instance, **kwargs):
    default_user = fake_user()
    WorkRecord.objects.filter(created_by=instance).update(created_by=default_user)


# Nuqson rekordi modeli (direktor yordamchisi tomonidan kiritiladi)
class DefectRecord(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    defect = models.ForeignKey(Defect, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, related_name='defect_records_created', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.employee} - {self.defect} - {self.quantity}'

@receiver(pre_delete, sender=User)
def set_default_created_by(sender, instance, **kwargs):
    default_user = fake_user()
    DefectRecord.objects.filter(created_by=instance).update(created_by=default_user)
