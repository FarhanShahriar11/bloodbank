from django.contrib import admin
from .models import *
# Register your models here.


class DonationInline(admin.TabularInline):
    model = Donation
    extra = 0
    readonly_fields = ('group', 'date', )
    fk_name = 'donor'

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile', 'mobile2', 'group', 'last_donated', 'is_eligible',)
    list_filter = ('group', 'last_donated',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'mobile', 'mobile2', 'group',)
    ordering = ('group', 'last_donated',)
    inlines = [DonationInline, ]

admin.site.register(Profile, ProfileAdmin)


class DonationAdmin(admin.ModelAdmin):
    list_display = ('group', 'donor', 'hospital', 'date', 'reciever',)
    list_filter = ('group', 'date',)
    search_fields = ('donor__user__username', 'donor__user__first_name', 'donor__user__last_name', 'group', 'hospital', 'reciever__user__username', 'reciever__user__first_name', 'reciever__user__last_name',)
    ordering = ('group', 'date',)


admin.site.register(Donation, DonationAdmin)


class RequestAdmin(admin.ModelAdmin):
    list_display = ('requested_by', 'group', 'hospital', 'patient_age', 'reason', 'emergency', 'date_time' )
    list_filter = ('group', 'patient_age',)
    search_fields = ('requested_by__user__username', 'requested_by__user__first_name', 'requested_by__user__last_name', 'group', 'patient_name', 'hospital', 'patient_age',)
    ordering = ('group', 'patient_age',)


admin.site.register(Request, RequestAdmin)


class StockAdmin(admin.ModelAdmin):
    list_display = ('group',)
    list_filter = ('group',)
    search_fields = ('group',)


admin.site.register(Stock, StockAdmin)