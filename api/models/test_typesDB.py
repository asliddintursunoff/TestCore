from django.db import models

class AllTestTypes(models.Model):
    test_type = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    image_url = models.ImageField(upload_to="media/testtypes",null=True,blank=True)
    link_for_test = models.CharField(max_length=200)
    

    def __str__(self):
        return f"{self.test_type} - {self.description[:20]}"