from rest_framework import serializers
from .models import Invoice, InvoiceDetail

class InvoiceDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for InvoiceDetail model.

    Maps the InvoiceDetail model fields to JSON fields for serialization and deserialization.
    """
    class Meta:
        model = InvoiceDetail
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    """
    Serializer for Invoice model.

    Maps the Invoice model fields to JSON fields for serialization and deserialization.
    Includes nested serialization of related InvoiceDetail instances.
    """
    invoice_details = InvoiceDetailSerializer(many=True, read_only=True, allow_null=True)

    class Meta:
        model = Invoice
        fields = ('id', 'date', 'invoice_number', 'customer_name', 'invoice_details')