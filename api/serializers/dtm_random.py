# api/serializers/dtm_random.py
from rest_framework import serializers
from api.models.dtm_TEST import DTM_Subjects, DTM_Test_Language, Test, Question, Answer

# ---------- Options (dropdowns) ----------
class SubjectOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DTM_Subjects
        fields = ("id", "subject_name", "test_type")

class LanguageOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DTM_Test_Language
        fields = ("id", "language")

# ---------- POST request (IDs) ----------
class DTMTestFilterByIdSerializer(serializers.Serializer):
    filter_type = serializers.IntegerField(min_value=1, max_value=3)
    language_id = serializers.IntegerField()
    first_subject_id = serializers.IntegerField()
    second_subject_id = serializers.IntegerField(required=False)

    def validate(self, attrs):
        ft = attrs.get("filter_type")
        if ft in (1, 2) and "second_subject_id" not in attrs:
            raise serializers.ValidationError({"second_subject_id": "Required for filter_type 1 and 2."})
        return attrs

# ---------- Nested QA for Retrieve ----------
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ("id", "answer", "answer_picture", "is_true")

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, source="DTManswers")

    class Meta:
        model = Question
        fields = ("id", "question", "question_img", "answers")
