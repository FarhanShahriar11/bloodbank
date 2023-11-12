from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date, timedelta

BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]

class Profile(models.Model):
    user = models.OneToOneField(User,related_name='profile', on_delete=models.SET_NULL, null=True, blank=True)
    group = models.CharField(max_length=10, choices=BLOOD_GROUP_CHOICES)
    mobile = models.CharField(max_length=11)
    mobile2 = models.CharField(max_length=11, null=True, blank=True)
    institution = models.CharField(max_length=100, null=True, blank=True)
    last_donated = models.DateField(null=True, blank=True)

    def __str__(self):
        if self.user:
            return self.user.get_full_name() if self.user.first_name else self.user.username
        else:
            return self.mobile

    def is_eligible(self):
        if not self.last_donated:
            return True
        return (date.today() - self.last_donated).days >= 90
    

class Donation(models.Model):
    group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, null=True, blank=True)
    request = models.ForeignKey('Request', related_name='donations', on_delete=models.SET_NULL, null=True, blank=True)
    donor = models.ForeignKey(Profile, related_name='donations', on_delete=models.CASCADE)
    hospital = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(default=date.today, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    reciever = models.ForeignKey(Profile, related_name='recieves', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.group} on {self.date}'

    def save(self, *args, **kwargs):
        if not self.group:
            self.group = self.donor.group
        self.donor.last_donated = self.date
        super().save(*args, **kwargs)


class Request(models.Model):
    BLOOD_TYPE_CHOICES = [
        ('Whole Blood', 'Whole Blood'),
        ('Platelets', 'Platelets'),
        ('Plasma', 'Plasma'),
    ]
    requested_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    patient_name = models.CharField(max_length=100)
    hospital = models.CharField(max_length=100)
    patient_age = models.PositiveIntegerField()
    reason = models.TextField()
    units_required = models.PositiveIntegerField(default=1)
    request_date = models.DateTimeField(auto_now_add=True)
    units_received = models.PositiveIntegerField(default=0)
    is_fulfilled = models.BooleanField(default=False)
    emergency = models.BooleanField(default=False)
    blood_type = models.CharField(max_length=20, choices=BLOOD_TYPE_CHOICES, default='Whole Blood')
    date_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Request from {self.requested_by} for {self.units_required} units of {self.group}"
    
    def save(self, *args, **kwargs):
        if self.units_received >= self.units_required:
            self.is_fulfilled = True
        super().save(*args, **kwargs)


class Stock(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Expired', 'Expired'),
        ('Used', 'Used'),
    ]
    group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    donor = models.ForeignKey(Profile, related_name='stocks', on_delete=models.SET_NULL, null=True, blank=True)
    donation = models.OneToOneField(Donation, related_name='stock', on_delete=models.SET_NULL, null=True, blank=True)
    receiver = models.ForeignKey(Profile, related_name='recieved_stocks', on_delete=models.SET_NULL, null=True, blank=True)
    donated = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Available')
    def __str__(self):
        return f"{self.group} expires on {self.expiry_date}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expiry_date = self.donated + timedelta(days=42)
        else:
            print(self.expiry_date)
            if self.receiver:
                self.status = 'Used'
            elif self.expiry_date and self.expiry_date.date() < date.today():
                self.status = 'Expired'
        super().save(*args, **kwargs)

    def is_expired(self):
        return self.expiry_date and self.expiry_date < date.today()

