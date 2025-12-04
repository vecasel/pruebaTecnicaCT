from django.contrib import admin
from .models import DocumentType, Client, Purchase

@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'document_type', 'document_number', 'email', 'phone')
    search_fields = ('document_number', 'first_name', 'last_name', 'email')


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('client', 'amount', 'purchase_date', 'order_number')
    list_filter = ('purchase_date',)
