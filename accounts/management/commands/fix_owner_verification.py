from django.core.management.base import BaseCommand
from accounts.models import User, OwnerProfile

class Command(BaseCommand):
    help = 'Fix owner verification status'

    def handle(self, *args, **kwargs):
        # Get all owner profiles with approved status
        approved_profiles = OwnerProfile.objects.filter(verification_status='approved')
        
        for profile in approved_profiles:
            if not profile.user.is_verified:
                profile.user.is_verified = True
                profile.user.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Fixed verification status for owner: {profile.user.username}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Owner already verified: {profile.user.username}'
                    )
                )
        
        # Check for any inconsistencies
        verified_users = User.objects.filter(is_verified=True, user_type='owner')
        for user in verified_users:
            try:
                profile = user.ownerprofile
                if profile.verification_status != 'approved':
                    self.stdout.write(
                        self.style.WARNING(
                            f'Inconsistent status for {user.username}: User verified but profile not approved'
                        )
                    )
            except OwnerProfile.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f'Verified owner {user.username} has no profile'
                    )
                ) 