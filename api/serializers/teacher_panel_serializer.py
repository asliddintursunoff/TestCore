from rest_framework import serializers
from rest_framework.reverse import reverse
from api.models.ClassicTestDB import ClassicTestDB


# for posting Test Submission
class TeacherPanelsTestDetailSerializer(serializers.Serializer):
    students_number = serializers.IntegerField()
    average_score = serializers.FloatField()
    average_time = serializers.IntegerField()


class ShareTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassicTestDB
        fields = ["id","qr_code_picture","unique_code"]
    