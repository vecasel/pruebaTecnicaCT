from rest_framework import serializers
from .models import Client, Purchase, DocumentType


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ['code', 'name']


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['amount', 'purchase_date', 'description', 'order_number']


class ClientSerializer(serializers.ModelSerializer):
    document_type = DocumentTypeSerializer()
    purchases = PurchaseSerializer(many=True)

    class Meta:
        model = Client
        fields = [
            'document_type',
            'document_number',
            'first_name',
            'last_name',
            'email',
            'phone',
            'purchases',
        ]
