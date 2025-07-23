from django.db import models
from .userDB import User
from .international_university_testDB import TestDB ,QuestionDB,AnswerDB

status_choices = [
    ("pass","Pass"),
    ("fail","Fail"),
    ("best","Best"),
    ("better","Better"),
    ("good","Good"),
    ("worst","Worst")
]   
class TestSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(TestDB, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    total_correct = models.IntegerField(default=0)
    status = models.CharField(choices=status_choices,max_length=10,default="better")
    score = models.FloatField(default=0)
    XP = models.IntegerField(default=0)
    time_taken = models.IntegerField(default=0)

    class Meta:
        #unique_together = ('user', 'test')
        verbose_name = "Test Submission"
        verbose_name_plural = "Test Submissions"

    def save(self, *args,**kwargs):
        
        if self.score >=30 and self.score < 60:
            self.status = "good"
        elif self.score >=60 and self.score < 85:
            self.status = "better"
        elif self.score >= 85 and self.score <=100:
            self.status = "best" 
        else:
            self.status = "worst"
        return super().save(*args,**kwargs)
    def __str__(self):
        return f"{self.user} - {self.test.test_name}"
class AnswerSubmission(models.Model):
    submission = models.ForeignKey(TestSubmission, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionDB, on_delete=models.CASCADE)
    chosen_answer = models.ForeignKey(AnswerDB, on_delete=models.CASCADE,null=True,blank=True)
    is_correct_answer = models.BooleanField(default=False)
    