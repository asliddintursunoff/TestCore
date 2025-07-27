from celery import shared_task
from django.utils import timezone
from api.models.userDB import User, Tariff

@shared_task
def reset_expired_tariffs():
    now = timezone.now()
    free_tariff = Tariff.objects.filter(is_free=True).first()

    if not free_tariff:
        return "❌ No free tariff defined."

    users_to_reset = User.objects.filter(
        tariff_expiry__lt=now,
    ).exclude(active_tariff=free_tariff)

    count = 0
    for user in users_to_reset:
        user.active_tariff = free_tariff
        user.tariff_expiry = None
        user.save(update_fields=["active_tariff", "tariff_expiry"])
        count += 1

    return f"✅ Reset {count} users to free plan"
