from django.db import models


    
class UniversityDB(models.Model):
    university_name = models.CharField(max_length=200)
    university_short_name = models.CharField(max_length=200)
    university_picture = models.ImageField(upload_to="media/universities")

    class Meta:
        verbose_name = "Xalqaro Universitet"
        verbose_name_plural = "Xalqaro Universitetlar"
    
    def __str__(self):
        return f"ID: {self.id} -  name: {self.university_name}"
class FacultyDB(models.Model):
    university = models.ForeignKey(UniversityDB,on_delete=models.CASCADE, related_name="faculties")
    faculty_name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return f"ID: {self.id} -  name: {self.faculty_name}"

