from django.contrib import admin

from orders.models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'status')
    fields = (
        'id', 'created',
        ('first_name', 'last_name'),
        ('email', 'address'),
        'basket_history', 'status', 'initiator'
    )
    list_filter = ('status', 'created')
    list_display_links = ('first_name',)
    search_fields = ('first_name',)
    readonly_fields = ('id', 'created')

