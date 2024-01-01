from django.urls import path
from invoices.views import InvoiceListCreateAPIView, InvoiceRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('invoices/', InvoiceListCreateAPIView.as_view(), name='invoice-list-create'),
    path('invoices/<int:pk>/', InvoiceRetrieveUpdateDestroyAPIView.as_view(), name='invoice-retrieve-update-destroy'),
]
