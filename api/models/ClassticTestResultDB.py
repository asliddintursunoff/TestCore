from django.db import models
from .ClassicTestDB import User,ClassicTestDB,ClassicQuestionDB,ClassicAnswerDB

class ClassicTestSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(ClassicTestDB, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    total_score = models.FloatField(default=0)
    total_correct = models.IntegerField()
    XP = models.IntegerField(default=0)
    time_taken = models.IntegerField(default=0)
    

    class Meta:
        #unique_together = ('user', 'test')
        verbose_name = "classic Test Submission"
        verbose_name_plural = "Classic Test Submissions"

    def __str__(self):
        return f"ID: {self.id} -- {self.user} - {self.test.dtm_test_name}"
class ClassicSubjectsSubmissionDB(models.Model):
    submission = models.ForeignKey(ClassicTestSubmission, related_name='dtm_submission_subject', on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    total_correct_answered = models.IntegerField(default=0)
    subject_id = models.IntegerField(default=0)
    
class ClassicAnswerSubmission(models.Model):
    submission_subject = models.ForeignKey(ClassicSubjectsSubmissionDB, related_name='submission_answers', on_delete=models.CASCADE)
    question = models.ForeignKey(ClassicQuestionDB, on_delete=models.CASCADE)
    chosen_answer = models.ForeignKey(ClassicAnswerDB, on_delete=models.CASCADE,null=True,blank=True)
    is_correct_answer = models.BooleanField(default=False)
