from django.db import models

class DTMTestGroups(models.Model):
    group_name = models.CharField(max_length=200)
    subject1 = models.CharField(max_length=200)
    subject2 = models.CharField(max_length=200)
    def __str__(self):
        return self.group_name
    
    class Meta:
        verbose_name = "Dtm Test Guruhlari"
        verbose_name_plural = "Dtm Test Guruhlari"
    


class DTMTestDB(models.Model):
    dtm_test_group = models.ForeignKey(DTMTestGroups,
                                       on_delete=models.CASCADE,
                                       related_name="DTMtests")
    dtm_test_name = models.CharField(max_length=200)
    test_description = models.TextField(blank=True)
    XP = models.IntegerField(default=0)
    time = models.PositiveIntegerField(default=0, help_text="Time in minutes")
    class Meta:
        verbose_name = "Dtm Test"
        verbose_name_plural = "Dtm Testlar"
    
    def __str__(self):
        return f"{self.dtm_test_name}.  Test Guruhi: {self.dtm_test_group}. XP = {self.XP}"

class DTMSubject(models.Model):
    dtm_test = models.ForeignKey(
        DTMTestDB, on_delete=models.CASCADE, related_name="DTMsubjects"
    )
    subject_name = models.CharField(max_length=200)
    subject_score = models.FloatField(default=3.1)

    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.subject_name} (DTM Test: {self.dtm_test.dtm_test_name})"



class DTMQuestionDB(models.Model):
    subject = models.ForeignKey(
        DTMSubject, on_delete=models.CASCADE, related_name="DTMquestions"
    )
    question = models.TextField()
    question_img = models.ImageField(
        upload_to="DTMquestions/", null=True, blank=True
    )

    def __str__(self):
        return f"Question {self.id} - {self.subject.subject_name}"
        


class DTMAnswerDB(models.Model):
    question = models.ForeignKey(
        DTMQuestionDB, on_delete=models.CASCADE, related_name="DTManswers"
    )
    answer = models.TextField()
    answer_picture = models.ImageField(
        upload_to="DTManswers/", null=True, blank=True
    )
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer to Question {self.question.id} - {'✅' if self.is_true else '❌'}"
