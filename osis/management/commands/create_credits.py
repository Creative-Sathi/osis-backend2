# your_app/management/commands/create_credits.py

from django.core.management.base import BaseCommand
from profileseller.models import Seller
from admindashboard.models import Credit  

class Command(BaseCommand):
    help = 'Create Credit instances for existing Approved sellers'

    def handle(self, *args, **options):
        approved_sellers = Seller.objects.filter(status='Approved')
        for seller in approved_sellers:
            # Check if Credit instance already exists for the seller
            if not Credit.objects.filter(seller_profile=seller).exists():
                Credit.objects.create(seller_profile=seller)
        self.stdout.write(self.style.SUCCESS('Credits created successfully'))
