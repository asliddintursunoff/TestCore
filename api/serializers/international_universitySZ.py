from api.models.international_universityDB import *
from rest_framework import serializers





class UniversitySerializer(serializers.ModelSerializer):
    university_name = serializers.CharField(help_text="Full name of the university")
    university_short_name = serializers.CharField(help_text="Short abbreviation (e.g., MIT)")
    university_picture = serializers.ImageField(help_text="University logo or image")

    class Meta:
        model = UniversityDB
        fields = "__all__"


class FacultyBaseSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(help_text="Name of the faculty (e.g., Computer Science)")
    description = serializers.CharField(help_text="Brief description of the faculty")

    class Meta:
        model = FacultyDB
        fields = "__all__"


class FacultiesSerializer(serializers.ModelSerializer):
    faculties = serializers.SerializerMethodField(help_text="List of faculties belonging to this university")
    total_faculty_numbers = serializers.SerializerMethodField()
    class Meta:
        model = UniversityDB
        fields = '__all__'
    

    
    def get_faculties(self, obj):
        faculty = FacultyDB.objects.filter(university=obj)
        return FacultyBaseSerializer(faculty, many=True).data
    
    def get_total_faculty_numbers(self,obj):
        faculty_numbers = FacultyDB.objects.filter(university=obj).count()
        return faculty_numbers