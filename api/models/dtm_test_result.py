from django.db import models 
from .userDB import User
from .DTMtestDB import (DTMTestDB,DTMAnswerDB,DTMQuestionDB)


class DTMTestSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(DTMTestDB, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    total_score = models.FloatField(default=0)
    XP = models.IntegerField(default=0)
    time_taken = models.IntegerField(default=0)

    class Meta:
        #unique_together = ('user', 'test')
        verbose_name = "DTM Test Submission"
        verbose_name_plural = "DTM Test Submissions"

    def __str__(self):
        return f"ID: {self.id} -- {self.user} - {self.test.dtm_test_name}"
class DTMSubjectsSubmissionDB(models.Model):
    submission = models.ForeignKey(DTMTestSubmission, related_name='dtm_submission_subject', on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    total_correct_answered = models.IntegerField(default=0)
    dtm_subject_id = models.IntegerField(default=0)
    
class DTMAnswerSubmission(models.Model):
    submission_subject = models.ForeignKey(DTMSubjectsSubmissionDB, related_name='submission_answers', on_delete=models.CASCADE)
    question = models.ForeignKey(DTMQuestionDB, on_delete=models.CASCADE)
    chosen_answer = models.ForeignKey(DTMAnswerDB, on_delete=models.CASCADE,null=True,blank=True)
    is_correct_answer = models.BooleanField(default=False)
