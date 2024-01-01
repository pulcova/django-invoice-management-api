from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status
from rest_framework.response import Response
from .models import Invoice, InvoiceDetail
from .serializers import InvoiceSerializer, InvoiceDetailSerializer
from rest_framework.generics import get_object_or_404

class InvoiceListCreateAPIView(ListCreateAPIView):
    """
    Endpoint for creating and listing invoices.

    Inherits:
        ListCreateAPIView: Provides GET (list) and POST (create) methods for invoices.
    """
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def get(self, request, *args, **kwargs):
        # Implement the GET method to retrieve a list of invoices
        invoices = self.queryset
        serializer = self.serializer_class(invoices, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
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
    Endpoint for retrieving, updating, and deleting individual invoices.

    Inherits:
        RetrieveUpdateDestroyAPIView: Provides GET (retrieve), PUT (update), PATCH (partial update),
        and DELETE (destroy) methods for individual invoices.
    """
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def get(self, request, *args, **kwargs):
        # Implement the GET method to retrieve an individual invoice
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        # Implement the PUT method to fully update an individual invoice
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        """
        Partially update an existing invoice and its details.

        Args:
            request: HTTP request containing partially updated invoice data.
            kwargs: Additional keyword arguments.

        Returns:
            Response: JSON response with the partially updated invoice data or error messages.
        """
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        # Implement the DELETE method to delete an individual invoice
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
