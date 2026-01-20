from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Medicine, MedicineLog

# Groups restored for Caregiver/Role management

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'dosage_amount', 'dosage_unit', 'frequency_amount', 'frequency_unit', 'user', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('name', 'user__username')

@admin.register(MedicineLog)
class MedicineLogAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'date', 'taken', 'taken_at')
    list_filter = ('date', 'taken')
