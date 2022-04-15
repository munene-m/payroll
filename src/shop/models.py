from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from .utils import generate_uuid_code

# Create your models here.

class Gender(models.TextChoices):
    MALE='male'
    FEMALE= 'female'
    OTHERS= 'others'

class Status(models.TextChoices):
    APPROVED='approved'
    PENDING= 'pending'
    DECLINED= 'declined'



class Employee(models.Model):
    
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=200, blank=True, null=True)
    mobile = models.CharField(max_length=15)
    address = models.TextField(max_length=100, default='')
    gender=models.CharField(max_length=50, choices=Gender.choices) 
    avatar = models.ImageField(default="avatar.png",  upload_to="avatars/")
    bank = models.CharField(max_length=25, default='Equity Bank Ke')
    salary = models.CharField(max_length=16,default='00.00') 
    slug = models.SlugField(unique=True, blank=True, max_length=500)
    modified = models.DateTimeField(auto_now=True)
    joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Employee."""

        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def __str__(self):
        return self.user.username

    def get_display_name(self):
        return f"{self.first_name} {self.last_name}"

    __initial_first_name = None
    __initial_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_first_name = self.first_name
        self.__initial_last_name = self.last_name
    
    def save(self, *args, **kwargs):
        """Save method for Profiles."""
        ex =False
        slug = self.slug
        if self.first_name != self.__initial_first_name or self.last_name != self.__initial_last_name or self.slug =="":
            if self.first_name and self.last_name:
                slug= slugify(str(self.first_name)+" "+(self.last_name))
                ex = Employee.objects.filter(slug=slug).exists()
                while ex:
                    slug=slugify(slug+" "+ str(generate_uuid_code()))
                    ex = Employee.objects.filter(slug=slug).exists()
            else:
                slug = str(self.user.username)
        self.slug = slug
        super().save( *args, **kwargs)


class Leave (models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    start = models.CharField(blank=False, max_length=15)
    end = models.CharField(blank=False, max_length=15)
    reason=models.TextField(max_length=200, blank=True, null=True)
    status = models.CharField(choices=Status.choices,  default=Status.PENDING, max_length=15)

    def __str__(self):
        return f"{self.employee} {self.start}"

    def approve(self):
        print(self.status)
        approve =self.status = Status.APPROVED
        print(approve)
        return approve

