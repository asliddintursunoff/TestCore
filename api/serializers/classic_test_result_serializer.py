from rest_framework import serializers
from rest_framework.reverse import reverse


# for posting Test Submission
class TeacherPanelsTestDetailSerializer(serializers.Serializer):
    students_number = serializers.IntegerField()
    average_score = serializers.FloatField()
    average_time = serializers.IntegerField()

    