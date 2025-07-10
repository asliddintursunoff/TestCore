from rest_framework import serializers
from rest_framework.reverse import reverse


# for posting Test Submission
class AnswerSubmission(serializers.Serializer):
    question_id = serializers.IntegerField()
    chosen_answer_id = serializers.IntegerField()

class TestSubmissionSerializer(serializers.Serializer):
    test_id = serializers.IntegerField()
    time_taken = serializers.IntegerField()
    answers = AnswerSubmission(many = True)


#for getting test results
class SubmittedAnswerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    answer = serializers.CharField()
    answer_picture = serializers.ImageField()
    is_true_answer = serializers.BooleanField()
    
    


class SubmittedQuestionsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    question = serializers.CharField()
    question_img = serializers.ImageField()
    chosen_answer_id = serializers.IntegerField()
    answered_correctly = serializers.BooleanField()
    ai_solution_info = serializers.SerializerMethodField()

    answers = SubmittedAnswerSerializer(many=True,read_only=True)
    

    def get_ai_solution_info(self, obj):
        request = self.context.get('request', None)
        return {
            "method": "POST",
            "endpoint": reverse("getting_result", kwargs={"question_id": obj["id"],"test_type_id":1}, request=request),
            "payload": {}
        }

class SubmittedSubjectSerializer(serializers.Serializer):
    subject_name = serializers.CharField()
    questions = SubmittedQuestionsSerializer(many=True,read_only=True)
    
    
    
class SubmittedTestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    test_name = serializers.CharField()
    time_for_test = serializers.IntegerField()
    time_taken = serializers.IntegerField()
    total_correct_answer = serializers.IntegerField()
    total_questions = serializers.IntegerField()
    XP_earned = serializers.IntegerField()
    subjects = SubmittedSubjectSerializer(many=True,read_only = True)

    