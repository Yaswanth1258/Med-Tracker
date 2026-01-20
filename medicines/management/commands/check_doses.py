from django.core.management.base import BaseCommand
from django.utils import timezone
from medicines.models import Medicine
import datetime

class Command(BaseCommand):
    help = 'Checks for overdue medicines and sends notifications'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        self.stdout.write(f"Checking doses at {now}...")

        medicines = Medicine.objects.all()
        
        for medicine in medicines:
            # Find the last time it was taken
            last_log = medicine.logs.filter(taken=True).order_by('-taken_at').first()
            
            if not last_log:
                # If never taken, assume it's due correctly (or logic could differ)
                # For now, let's skip or remind to start
                self.stdout.write(self.style.WARNING(f"Medicine {medicine.name} has no history. Remind to start?"))
                continue

            last_taken = last_log.taken_at
            if not last_taken:
                 continue

            # Calculate frequency delta
            if medicine.frequency_unit.lower().startswith('hour'):
                delta = datetime.timedelta(hours=medicine.frequency_amount)
            elif medicine.frequency_unit.lower().startswith('day'):
                delta = datetime.timedelta(days=medicine.frequency_amount)
            else:
                # Default fallback or error
                delta = datetime.timedelta(hours=24)

            next_dose = last_taken + delta

            if now >= next_dose:
                # IT IS TIME!
                user_email = medicine.user.email
                self.stdout.write(self.style.SUCCESS(f"NOTIFICATION: Time to take {medicine.name}! (Due at {next_dose.strftime('%H:%M')}) -> Sending to {user_email}"))
                # Here we would call send_mail()
            else:
                time_left = next_dose - now
                self.stdout.write(f"Medicine {medicine.name} is OK. Next dose in {time_left}.")
