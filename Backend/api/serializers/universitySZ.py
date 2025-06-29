from api.models.universityDB import *
from rest_framework import serializers

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversityDB
        fields = ["id","university_name","university_short_name","university_picture"]


class FacultyBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacultyDB
        fields = ["id","faculty_name","description"]


class FacultiesSerializer(serializers.ModelSerializer):
    faculties = serializers.SerializerMethodField()
    class Meta:
        model = UniversityDB
        fields = ["university_name","university_short_name","university_picture","faculties"] 

    def get_faculties(self,obj):
        faculty = FacultyDB.objects.filter(university = obj)
        return FacultyBaseSerializer(faculty,many = True).data
