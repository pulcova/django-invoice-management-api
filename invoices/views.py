from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status
from rest_framework.response import Response
from .models import Invoice, InvoiceDetail
from .serializers import InvoiceSerializer, InvoiceDetailSerializer
from rest_framework.generics import get_object_or_404

class InvoiceListCreateAPIView(ListCreateAPIView):
    """
    API endpoint that allows creating and listing invoices.

    Inherits:
        ListCreateAPIView: Provides GET (list) and POST (create) methods for invoices.
    """
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new invoice with its details.

        Args:
            request: HTTP request containing invoice data.

        Returns:
            Response: JSON response with the created invoice data or error messages.
        """
        invoice_data = request.data
        invoice_serializer = self.get_serializer(data=invoice_data)
        if invoice_serializer.is_valid():
            invoice = invoice_serializer.save()
            invoice_details_data = request.data.get('invoice_details', [])
            for detail_data in invoice_details_data:
                detail_data['invoice'] = invoice.pk
            detail_serializer = InvoiceDetailSerializer(data=invoice_details_data, many=True)
            if detail_serializer.is_valid():
                detail_serializer.save()
                return Response(invoice_serializer.data, status=status.HTTP_201_CREATED)
        return Response(invoice_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InvoiceRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows retrieving, updating, and deleting individual invoices.

    Inherits:
        RetrieveUpdateDestroyAPIView: Provides GET (retrieve), PUT (update), PATCH (partial update),
        and DELETE (destroy) methods for individual invoices.
    """
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def update(self, request, *args, **kwargs):
        """
        Update an existing invoice and its details.

        Args:
            request: HTTP request containing updated invoice data.
            kwargs: Additional keyword arguments.

        Returns:
            Response: JSON response with the updated invoice data or error messages.
        """
        instance = self.get_object()
        invoice_data = request.data

        # Serialize the existing instance with the updated data
        invoice_serializer = self.get_serializer(instance, data=invoice_data, partial=True)
        if invoice_serializer.is_valid():
            # Save the updated invoice data
            invoice = invoice_serializer.save()

            # Get the existing invoice details related to this invoice
            existing_details = InvoiceDetail.objects.filter(invoice=invoice)

            # Iterate through the incoming details data
            incoming_details_data = request.data.get('invoice_details', [])
            for detail_data in incoming_details_data:
                # Check if the detail exists in the database
                if 'id' in detail_data:
                    detail_instance = get_object_or_404(existing_details, id=detail_data['id'])
                    detail_serializer = InvoiceDetailSerializer(detail_instance, data=detail_data, partial=True)
                else:
                    # Create new detail if 'id' not provided
                    detail_data['invoice'] = invoice.pk
                    detail_serializer = InvoiceDetailSerializer(data=detail_data)

                if detail_serializer.is_valid():
                    detail_serializer.save()

            return Response(invoice_serializer.data, status=status.HTTP_200_OK)

        return Response(invoice_serializer.errors, status=status.HTTP_400_BAD_REQUEST)