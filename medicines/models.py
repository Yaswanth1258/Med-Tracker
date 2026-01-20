from django.db import models
from django.contrib.auth.models import User

class Medicine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medicines')
    name = models.CharField(max_length=200)
    dosage_amount = models.PositiveIntegerField(help_text="Amount of dosage (e.g., 500)")
    dosage_unit = models.CharField(max_length=50, help_text="Unit of dosage (e.g., mg, ml, pill)")
    frequency_amount = models.PositiveIntegerField(help_text="Frequency amount (e.g., every 6)")
    frequency_unit = models.CharField(max_length=50, help_text="Frequency unit (e.g., hours, days)")
    time_of_day = models.TimeField(help_text="Time to take the medicine", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.dosage_amount}{self.dosage_unit})"

class MedicineLog(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='logs')
    date = models.DateField()
    taken = models.BooleanField(default=False)
    taken_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['medicine', 'date']

    def __str__(self):
        return f"{self.medicine.name} - {self.date} - {'Taken' if self.taken else 'Missed'}"
