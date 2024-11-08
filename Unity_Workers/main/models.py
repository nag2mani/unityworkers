from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class Cards(models.Model):
    heading = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='images/card')
    price = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.heading


class WorkerType(models.Model):
    name = models.CharField(max_length=1000)
    code = models.CharField(max_length=5,default='XX')

    def __str__(self):
        return self.name


class WorkerRegistration(AbstractUser):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('Married', 'Married'),
        ('Unmarried', 'Unmarried'),
        ('Widow', 'Widow'),
    ]
    password = models.CharField(max_length=128, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=100,blank=True,null=True,unique=True)
    full_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(null=True,blank=True,default=0)
    photo = models.ImageField(upload_to='photos/',blank=False, null=False)
    full_address = models.TextField(blank=True, null=True)
    district = models.CharField(max_length=100,blank=True, null=True)
    village = models.CharField(max_length=100, blank=True, null=True)
    tehsil = models.CharField(max_length=100,blank=True, null=True)
    pincode = models.CharField(max_length=6,blank=True, null=True)
    state = models.CharField(max_length=100,blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    mobile_number = models.CharField(max_length=15,blank=True, null=True)
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)

    # Update max_length to match longest value ('Other' is 5 characters)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)

    bank_branch_name = models.CharField(max_length=100,blank=True, null=True)
    ifsc_code = models.CharField(max_length=11,blank=True, null=True)
    bank_account_number = models.CharField(max_length=20,blank=True, null=True)
    bank_passbook_pdf = models.FileField(upload_to='bank_passbooks/',blank=True, null=True)
    aadhar_number = models.CharField(max_length=12)
    aadhar_card_pdf = models.FileField(upload_to='aadhar_cards/',blank=True, null=True)

    # Update max_length to match longest value ('Unmarried' is 9 characters)
    marital_status = models.CharField(max_length=9, choices=MARITAL_STATUS_CHOICES)

    education_qualification = models.CharField(max_length=100, blank=True, null=True)

    # Work experience should be a required field by default
    work_experience = models.PositiveIntegerField(blank=True, null=True)

    # Many-to-many field to allow selecting multiple worker types
    worker_type = models.ManyToManyField(WorkerType)

    def __str__(self):
        return self.full_name
    
    def set_password(self, raw_password):
        self.password = raw_password

    def get_full_name(self) -> str:
        return self.full_name  # Directly return the full_name field
    
    def get_full_name_and_username(self):
        return {
            "username": self.username or "Guest",
            "full_name": self.full_name or "No Name"
        }



class WorkRequest(models.Model):
    WORKER_TYPES = [
        ('electrician', 'Electrician'),
        ('painter', 'Painter'),
        ('plumber', 'Plumber'),
        ('majdur', 'Majdur'),
        ('rajgeer', 'Rajgeer'),
        ('other', 'Other'),
    ]

    full_name = models.CharField(max_length=255, null=True, blank=True)
    full_address = models.TextField(null=True, blank=True)
    landmark = models.CharField(max_length=255, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    date_of_work = models.DateField(null=True, blank=True)
    number_workers_required = models.IntegerField(null=True, blank=True)
    work_location_link = models.URLField(null=True, blank=True)
    worker_type = models.CharField(max_length=20, choices=WORKER_TYPES, null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.worker_type} - {self.time_created}"



class Contracts(models.Model):

    full_name = models.CharField(max_length=255, null=True, blank=True)
    full_address = models.TextField(null=True, blank=True)
    landmark = models.CharField(max_length=255, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    date_of_work = models.DateField(null=True, blank=True)
    type_of_work = models.TextField(null=True, blank=True)
    work_location_link = models.URLField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.type_of_work} - {self.time_created}"



class Worker_number(models.Model):
   worker_type = models.CharField(max_length=255, null=True, blank=True)
   worker_number = models.PositiveIntegerField(default=1)



