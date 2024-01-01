from django.db import models
from decimal import Decimal

class Invoice(models.Model):
    """
    Model representing an invoice.

    Attributes:
        date (DateField): The date of the invoice.
        invoice_number (CharField): The unique identifier for the invoice.
        customer_name (CharField): The name of the customer associated with the invoice.

    Methods:
        __str__: Returns a string representation of the invoice.
    """
    date = models.DateField()
    invoice_number = models.CharField(max_length=100, unique=True)
    customer_name = models.CharField(max_length=255)
    
    def __str__(self):
        """
        Returns a string representation of the invoice.

        Returns:
            str: A string containing the invoice number.
        """
        return f"Invoice {self.invoice_number}"

class InvoiceDetail(models.Model):
    """
    Model representing details of an invoice.

    Attributes:
        invoice (ForeignKey): Reference to the related Invoice object.
        description (TextField): Description of the invoice detail.
        quantity (IntegerField): The quantity of items in the detail.
        unit_price (DecimalField): The price per unit of the item.
        price (DecimalField): The total price for this detail line.

    Methods:
        save: Calculates and sets the total price before saving the object.
        __str__: Returns a string representation of the invoice detail.
    """
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='invoice_details')
    description = models.TextField()
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):      
        """
        Overrides the save method to calculate the total price before saving the object.
        """
        self.price = Decimal(self.quantity) * Decimal(self.unit_price)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns a string representation of the invoice detail.

        Returns:
            str: A string containing the invoice number and description.
        """
        return f"{self.invoice.invoice_number} - {self.description}"