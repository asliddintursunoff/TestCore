from django.db import models
from .international_universityDB import FacultyDB



class TestDB(models.Model):

    faculty = models.ForeignKey(
        FacultyDB,null=True,blank=True,
        on_delete=models.CASCADE,
        related_name="tests"
    )
    test_name = models.CharField(max_length=200)
    time = models.PositiveIntegerField(default=0, help_text="Time in minutes")
    test_description = models.TextField(blank=True)
    XP = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.test_name} ({self.faculty})"

    class Meta:
        verbose_name = "Xalqaro Universitet Testi"
        verbose_name_plural = "Xalqaro Universitet Testlari"
    

class Subject(models.Model):
    test = models.ForeignKey(
        TestDB, on_delete=models.CASCADE, related_name="subjects"
    )
    subject_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.subject_name} (Test: {self.test.test_name})"


class QuestionDB(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="questions"
    )
    question = models.TextField()
    question_img = models.ImageField(
        upload_to="questions/", null=True, blank=True
    )

    def __str__(self):
        return f"Question {self.id} - {self.subject.subject_name}"


class AnswerDB(models.Model):
    question = models.ForeignKey(
        QuestionDB, on_delete=models.CASCADE, related_name="answers"
    )
    answer = models.TextField()
    answer_picture = models.ImageField(
        upload_to="answers/", null=True, blank=True
    )
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer to Question {self.question.id} - {'✅' if self.is_true else '❌'}"
