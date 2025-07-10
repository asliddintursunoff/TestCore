from django.db import models

class Tariff(models.Model):
    tariff_name = models.CharField(max_length=200)
    tariff_price = models.FloatField(default=0)
    is_free = models.BooleanField(default=True)
    max_usage_of_solving_test = models.IntegerField(default=20)
    max_usage_of_creating_test_by_AI = models.IntegerField(default=2)
    is_accessed_teacher_panel = models.BooleanField()
    duration_days = models.PositiveIntegerField()  # e.g. 30 days
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.is_free = self.tariff_price == 0
        return super().save(*args, **kwargs)