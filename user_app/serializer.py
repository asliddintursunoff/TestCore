from rest_framework import serializers


class HeaderDataSerialzier(serializers.Serializer):
    user_tariff = serializers.CharField()
    user_tariff_free = serializers.BooleanField()
    user_xp = serializers.IntegerField()

    def get_user_xp(self, obj):
        return self.format_xp(obj.user_xp)

    def format_xp(self, xp):
        if xp >= 1_000_000:
            return f"{xp / 1_000_000:.1f}m"
        elif xp >= 1_000:
            return f"{xp / 1_000:.1f}k"
        return str(xp)
    
        