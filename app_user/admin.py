from django.contrib import admin

from .models import User, Account
# Register your models here.


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    search_fields = ['username']


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    search_fields = ['payment_type', 'payment_for']
    list_per_page = 20
    list_display = ['payment_for']
    list_filter = ['created', 'updated']



