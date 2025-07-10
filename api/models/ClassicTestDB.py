from django.db import models
from .userDB import User

class ClassicTestDB(models.Model):
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,default=True)
    test_name = models.CharField(max_length=200)
    time = models.PositiveIntegerField(default=0, help_text="Time in minutes")
    price_for_test = models.FloatField(default=0)
    is_olympiad_test = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.test_name} ({self.created_by})"

    class Meta:
        verbose_name = "Classic Test"
        verbose_name_plural = "Classic Testlar"
    

class ClassicSubject(models.Model):
    test = models.ForeignKey(
        ClassicTestDB, on_delete=models.CASCADE, related_name="subjects"
    )
    subject_name = models.CharField(max_length=200)
    point_for_each_question = models.FloatField(default=1)
    def __str__(self):
        return f"{self.subject_name} (Test: {self.test.test_name})"


class ClassicQuestionDB(models.Model):
    subject = models.ForeignKey(
        ClassicSubject, on_delete=models.CASCADE, related_name="questions"
    )
    question = models.TextField()
    question_img = models.ImageField(
        upload_to="questions/", null=True, blank=True
    )

    def __str__(self):
        return f"Question {self.id} - {self.subject.subject_name}"


class ClassicAnswerDB(models.Model):
    question = models.ForeignKey(
        ClassicQuestionDB, on_delete=models.CASCADE, related_name="answers"
    )
    answer = models.TextField()
    answer_picture = models.ImageField(
        upload_to="answers/", null=True, blank=True
    )
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer to Question {self.question.id} - {'✅' if self.is_true else '❌'}"
