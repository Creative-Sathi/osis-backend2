from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Order, Quotation  # Import your Order and Quotation models

@shared_task
def update_quotations_status():
    # Get the current time
    now = timezone.now()

    # Get all Orders that were created more than 10 minutes ago
    orders = Order.objects.filter(dateandtime__lte=now-timedelta(minutes=10))

    # Loop through each order
    for order in orders:
        # Get the attached quotation
        quotation = Quotation.objects.get(order_id=order.id)
        seller_quotation = quotation.seller_quotation
        specific_seller_quotation = SpecificSellerQuotation.objects.get(id=seller_quotation)
        
        

        # If the quotation's status is not 'Accepted', change it to 'Cancelled'
        if quotation.status == 'Pending':
            quotation.status = 'Rejected'
            quotation.remarks = 'No Update from Buyer'
            quotation.save()