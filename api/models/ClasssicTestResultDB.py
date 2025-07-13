from django.db import models
from ClassicTestDB import *

class ClassicTestSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(ClassicTestDB, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    total_correct = models.IntegerField(default=0)
    
    time_taken = models.IntegerField(default=0)

    class Meta:
        #unique_together = ('user', 'test')
        verbose_name = "Test Submission"
        verbose_name_plural = "Test Submissions"

    def __str__(self):
        return f"{self.user} - {self.test.test_name}"
class ClassicAnswerSubmission(models.Model):
    submission = models.ForeignKey(ClassicTestSubmission, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(ClassicQuestionDB, on_delete=models.CASCADE)
    chosen_answer = models.ForeignKey(ClassicAnswerDB, on_delete=models.CASCADE,null=True,blank=True)
    is_correct_answer = models.BooleanField(default=False)
    