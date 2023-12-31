# Django REST API for Invoices

This Django application provides REST API endpoints for managing invoices and their details.

## Setup

1. **Installation**

    ```bash
    pip install -r requirements.txt
    ```

2. **Database Setup**

    Make migrations and migrate the database:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

3. **Run the Server**

    Start the development server:

    ```bash
    python manage.py runserver
    ```

## Endpoints

### `/invoices/`

- **GET**: Retrieve a list of all invoices.
- **POST**: Create a new invoice. The payload should include `date`, `invoice_number`, and `customer_name` fields for the invoice. Additionally, you can provide `invoice_details` in the payload to create associated details.

### `/invoices/<int:pk>/`

- **GET**: Retrieve details of a specific invoice.
- **PUT**: Update details of a specific invoice.
- **DELETE**: Delete a specific invoice.

## Models

### `Invoice`

- Fields:
    - `date`: Date of the invoice.
    - `invoice_number`: Unique identifier for the invoice.
    - `customer_name`: Name of the customer associated with the invoice.

### `InvoiceDetail`

- Fields:
    - `invoice`: Foreign key referencing the associated Invoice.
    - `description`: Description of the invoice detail.
    - `quantity`: Quantity of items in the detail.
    - `unit_price`: Price per unit of the item.
    - `price`: Total price for this detail line.

## Testing

To run tests for the APIs, use the following command:

```bash
python manage.py test
