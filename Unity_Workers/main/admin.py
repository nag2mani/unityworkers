from django.contrib import admin
from .models import Cards, WorkerRegistration, WorkerType, WorkRequest, Contracts, Rapid_service

from django.db.models import Count

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

class WorkerTypeCountFilter(admin.SimpleListFilter):
    title = _('worker type count')  # Title shown in the filter
    parameter_name = 'worker_type_count'  # URL query parameter name

    def lookups(self, request, model_admin):
        """Define filter options"""
        return (
            ('single', _('Single Worker Type')),
            ('multiple', _('Multiple Worker Types')),
        )

    def queryset(self, request, queryset):
        """Filter queryset based on selected option"""
        if self.value() == 'single':
            return queryset.annotate(num_types=Count('worker_type')).filter(num_types=1)
        elif self.value() == 'multiple':
            return queryset.annotate(num_types=Count('worker_type')).filter(num_types__gt=1)
        return queryset





# Register the WorkerType model for easy addition from the admin
@admin.register(WorkerType)
class WorkerTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Register the WorkerRegistration model with customized display in the admin
@admin.register(WorkerRegistration)
class WorkerRegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'age', 'gender', 'marital_status', 'state', 'mobile_number')
    search_fields = ('full_name', 'mobile_number', 'aadhar_number')  # Allow search by name, mobile, and Aadhar
    list_filter = ('gender', WorkerTypeCountFilter,"worker_type")  # Filters for quick filtering in admin panel
    filter_horizontal = ('worker_type',)  # Enables horizontal filter for ManyToManyField

# Register the Cards model
@admin.register(Cards)
class CardsAdmin(admin.ModelAdmin):
    list_display = ('heading', 'description')


admin.site.register(Rapid_service)
admin.site.register(Contracts)