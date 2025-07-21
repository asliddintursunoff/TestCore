from django.db import models


    
class UniversityDB(models.Model):
    university_name = models.CharField(max_length=200)
    university_short_name = models.CharField(max_length=200)
    description = models.TextField(default=" ")
    university_picture = models.ImageField(upload_to="media/universities")
    university_img = models.ImageField(upload_to="media/universities",null=True,blank=True)
    contract_sum_start = models.IntegerField(default=0)
    contract_sum_finish = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=17)
    location = models.TextField(default="Tashkent")
    instagram_link = models.CharField(max_length=200,null=True,blank=True)
    telegram_link = models.CharField(max_length=200,null=True,blank=True)
    website_link = models.CharField(max_length=200,null=True,blank=True)

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

