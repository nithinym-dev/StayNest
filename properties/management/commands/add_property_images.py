from django.core.management.base import BaseCommand
from properties.models import Property, PropertyImage

class Command(BaseCommand):
    help = 'Add demo property images'

    def handle(self, *args, **options):
        properties = Property.objects.all()
        
        # Demo image URLs (you can replace with actual images)
        demo_images = [
            'https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=800',
            'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800',
            'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800',
            'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800',
            'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800'
        ]

        for i, property_obj in enumerate(properties):
            if not property_obj.images.exists():
                # You can download and save actual images here
                # For now, just create placeholders
                PropertyImage.objects.create(
                    property_obj=property_obj,
                    caption=f'{property_obj.name} - Main View',
                    is_primary=True
                )
                
                self.stdout.write(f'Added image placeholder for: {property_obj.name}')
