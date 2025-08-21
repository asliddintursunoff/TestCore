from django.db import models


dtm_test_choice = [
    ("main_subject", "Main Subject"),
    ("mandatory_subject","Mandatory Subject")
]

class DTM_Subjects(models.Model):
    subject_name = models.CharField(max_length=200)
    test_type = models.CharField(max_length=20,choices=dtm_test_choice)


    def __str__(self):
        return self.subject_name
class DTM_Test_Language(models.Model):
    language = models.CharField(max_length=200)
    def __str__(self):
        return self.language


class Test(models.Model):
    subject_name = models.ForeignKey(DTM_Subjects,on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    language = models.ForeignKey(DTM_Test_Language,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} - {self.subject_name} - {self.subject_name.test_type}"


class Question(models.Model):
    test= models.ForeignKey(
        Test, on_delete=models.CASCADE, related_name="DTMquestions"
    )
    question = models.TextField()
    question_img = models.ImageField(
        upload_to="DTMquestions/", null=True, blank=True
    )

    def __str__(self):
        return f"Question {self.id} - {self.test.subject_name}"
        


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="DTManswers"
    )
    answer = models.TextField()
    answer_picture = models.ImageField(
        upload_to="DTManswers/", null=True, blank=True
    )
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer to Question {self.question.id} - {'✅' if self.is_true else '❌'}"

