from rest_framework import serializers
# for posting Tests
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
    #get_answer_ai_link = serializers.HyperlinkedIdentityField(view_name='test-detail', lookup_field='pk')

    answers = SubmittedAnswerSerializer(many=True,read_only=True)


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

    