from rest_framework import serializers
from rest_framework.reverse import reverse


# for posting Test Submission
class DTMAnswerSubmissionSerializer(serializers.Serializer):
    question_id = serializers.IntegerField(help_text="ID of the question being answered")
    chosen_answer_id = serializers.IntegerField(help_text="ID of the chosen answer option")

class DTMSubjectSubmissionSerializer(serializers.Serializer):
    dtm_subject_id = serializers.IntegerField(help_text="ID of the subject within the test")
    answers = DTMAnswerSubmissionSerializer(many=True, help_text="List of answers submitted for this subject")

class DTMTestSubmissionSerializer(serializers.Serializer):
    test_id = serializers.IntegerField(help_text="ID of the test being submitted")
    time_taken = serializers.IntegerField(help_text="Time taken to complete the test (in seconds)")
    subjects = DTMSubjectSubmissionSerializer(many=True, help_text="Submitted answers grouped by subject")



#for getting test results
class DTMSubmittedAnswerSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text="Answer ID")
    answer = serializers.CharField(help_text="Answer text")
    answer_picture = serializers.ImageField(help_text="Image for the answer, if any")
    is_true_answer = serializers.BooleanField(help_text="Whether this answer is the correct one")


class DTMSubmittedQuestionsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    question = serializers.CharField()
    question_img = serializers.ImageField()
    chosen_answer_id = serializers.IntegerField()
    answered_correctly = serializers.BooleanField()
    ai_solution_info = serializers.SerializerMethodField(help_text="API link to get AI-generated solution")
    answers = DTMSubmittedAnswerSerializer(many=True,read_only=True)
    

    def get_ai_solution_info(self, obj):
        request = self.context.get('request', None)
        return {
            "method": "POST",
            "endpoint": reverse("getting_result", kwargs={"question_id": obj["id"],"test_type_id":2}, request=request),
            "payload": {}
        }

class DTMSubmittedSubjectSerializer(serializers.Serializer):
    subject_name = serializers.CharField()
    subject_score_for_each_question = serializers.FloatField()
    total_earned_score = serializers.FloatField()
    number_total_correct = serializers.FloatField()
    questions = DTMSubmittedQuestionsSerializer(many=True,read_only=True)
    
    
    
class DTMSubmittedTestSerializer(serializers.Serializer):
    dtm_test_id = serializers.IntegerField()
    test_name = serializers.CharField()
    time_for_test = serializers.IntegerField()
    time_taken = serializers.IntegerField()
    
    total_score = serializers.FloatField()
    total_questions = serializers.IntegerField()
    XP_earned = serializers.IntegerField()
    subjects = DTMSubmittedSubjectSerializer(many=True,read_only = True)

    