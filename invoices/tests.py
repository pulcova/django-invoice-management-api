from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Invoice, InvoiceDetail

class InvoiceRetrieveAPITest(TestCase):
    def setUp(self):
        """Set up initial data for invoice retrieval test."""
        self.client = APIClient()
        self.invoice = Invoice.objects.create(date='2023-01-01', invoice_number='INV-001', customer_name='Test Customer')
        self.invoice_detail = InvoiceDetail.objects.create(
            invoice=self.invoice, 
            description='This is the product of Test Customer',
            quantity=5,
            unit_price=10.99,
            price=54.95
        )

    def test_retrieve_invoice_with_details(self):
        """Test retrieving an invoice with its details."""
        response = self.client.get(reverse('invoice-retrieve-update-destroy', kwargs={'pk': self.invoice.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(response.data['date'], '2023-01-01')
        self.assertEqual(response.data['invoice_number'], 'INV-001')
        self.assertEqual(response.data['customer_name'], 'Test Customer')

        self.assertIn('invoice_details', response.data)
        invoice_details = response.data.get('invoice_details')
        if invoice_details:
            self.assertEqual(len(invoice_details), 1)  
            self.assertEqual(invoice_details[0]['description'], 'This is the product of Test Customer')
            self.assertEqual(invoice_details[0]['quantity'], 5)
            self.assertEqual(float(invoice_details[0]['unit_price']), 10.99)
            self.assertEqual(float(invoice_details[0]['price']), 54.95)
        

class InvoiceCreateAPITest(TestCase):
    def setUp(self):
        """Set up initial data for invoice creation test."""
        self.client = APIClient()
        self.invoice_data = {
            'date': '2023-01-01',
            'invoice_number': 'INV-002',
            'customer_name': 'New Test Customer'
        }

    def test_create_invoice(self):
        """Test creating a new invoice."""
        response = self.client.post(reverse('invoice-list-create'), self.invoice_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Invoice.objects.filter(date='2023-01-01').exists())
        self.assertTrue(Invoice.objects.filter(invoice_number='INV-002').exists())
        self.assertTrue(Invoice.objects.filter(customer_name='New Test Customer').exists())
        
class InvoiceUpdateAPITest(TestCase):
    def setUp(self):
        """Set up initial data for invoice update test."""
        self.client = APIClient()
        self.invoice = Invoice.objects.create(date='2023-01-01', invoice_number='INV-003', customer_name='Test Customer')
        self.update_data = {
            'date': '2023-02-01',
            'invoice_number': 'INV-003',
            'customer_name': 'Updated Test Customer'
        }

    def test_update_invoice(self):
        """Test updating an existing invoice."""
        response = self.client.put(reverse('invoice-retrieve-update-destroy', kwargs={'pk': self.invoice.pk}), self.update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_invoice = Invoice.objects.get(pk=self.invoice.pk)
        self.assertEqual(updated_invoice.customer_name, 'Updated Test Customer')


class InvoiceUpdateAPITest(TestCase):
    def setUp(self):
        """Set up initial data for partial invoice update test."""
        self.client = APIClient()
        self.invoice = Invoice.objects.create(date='2023-01-01', invoice_number='INV-003', customer_name='Test Customer')
        self.invoice_detail_1 = InvoiceDetail.objects.create(
            invoice=self.invoice,
            description='Product A',
            quantity=10,
            unit_price=25.00,
            price=250.00
        )
        self.invoice_detail_2 = InvoiceDetail.objects.create(
            invoice=self.invoice,
            description='Product B',
            quantity=10,
            unit_price=25.00,
            price=250.00
        )
        self.update_data = {
            'date': '2023-02-01',
            'invoice_number': 'INV-003',
            'customer_name': 'Updated Test Customer',
            'invoice_details': [
                {
                    'id': self.invoice_detail_1.id,
                    'description': 'Updated Product A',
                    'quantity': 20,
                    'unit_price': 30.00,
                    'price': 600.00,
                },
                {
                    'id': self.invoice_detail_2.id,
                    'description': 'Updated Product B',
                    'quantity': 15,
                    'unit_price': 20.00,
                    'price': 300.00,
                }
            ]
        }

    def test_partial_update_invoice_with_details(self):
        """Test partially updating an invoice with details."""
        response = self.client.patch(reverse('invoice-retrieve-update-destroy', kwargs={'pk': self.invoice.pk}), self.update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_invoice = Invoice.objects.get(pk=self.invoice.pk)
        self.assertEqual(updated_invoice.customer_name, 'Updated Test Customer')

        updated_detail_1 = InvoiceDetail.objects.get(pk=self.invoice_detail_1.pk)
        updated_detail_2 = InvoiceDetail.objects.get(pk=self.invoice_detail_2.pk)
        self.assertEqual(updated_detail_1.description, 'Updated Product A')
        self.assertEqual(updated_detail_1.quantity, 20)
        self.assertEqual(updated_detail_1.unit_price, 30.00)
        self.assertEqual(updated_detail_1.price, 600.00)
        self.assertEqual(updated_detail_2.description, 'Updated Product B')
        self.assertEqual(updated_detail_2.quantity, 15)
        self.assertEqual(updated_detail_2.unit_price, 20.00)
        self.assertEqual(updated_detail_2.price, 300.00)


class InvoiceDeleteAPITest(TestCase):
    def setUp(self):
        """Set up initial data for invoice deletion test."""
        self.client = APIClient()
        self.invoice = Invoice.objects.create(date='2023-01-01', invoice_number='INV-005', customer_name='Test Customer')

    def test_delete_invoice(self):
        """Test deleting an existing invoice."""
        response = self.client.delete(reverse('invoice-retrieve-update-destroy', kwargs={'pk': self.invoice.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Invoice.objects.filter(pk=self.invoice.pk).exists())

