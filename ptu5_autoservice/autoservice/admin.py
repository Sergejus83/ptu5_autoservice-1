from django.contrib import admin
from . import models


class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('service', 'quantity', 'price', 'total', 'order')
    ordering = ('order', 'id')
    list_filter = ('order', )


class OrderLineInline(admin.TabularInline):
    model = models.OrderLine
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineInline,)
    list_display = ('id', 'user', 'date', 'estimate_date', 'is_expired_date', 'total', 'car')
    list_filter = ('estimate_date', 'status')
    readonly_fields = ('id', 'is_expired_date')
    search_fields = ('id', 'plate', 'car', 'client')


class CarAdmin(admin.ModelAdmin):
    list_display = ('client', 'car_model', 'plate', 'vin')
    list_filter = ('client', 'car_model')
    search_fields = ('vin', 'plate')


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


admin.site.register(models.Car, CarAdmin)
admin.site.register(models.CarModel)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderLine, OrderLineAdmin)
