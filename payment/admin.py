

# Register your models here.
from django.contrib import admin
from paycomuz.models import Transaction

# Unregister the broken TransactionAdmin from the package
try:
    admin.site.unregister(Transaction)
except admin.sites.NotRegistered:
    pass

# Register a fixed version that avoids the broken fields
@admin.register(Transaction)
class FixedTransactionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Transaction._meta.fields]  # Safe dynamic display
