from rest_framework import serializers
from api.models.international_university_testDB import (
    TestDB,
    FacultyDB,
    AnswerDB,
    QuestionDB,
    Subject)




class TestBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestDB
        fields = ["id","test_name","time","test_description"]


class TestSerializer(serializers.ModelSerializer):
    tests = serializers.SerializerMethodField()
    
    class Meta:
        model = FacultyDB
        fields = ["faculty_name","description","tests"]
    def get_tests(self,obj):    
        test = TestDB.objects.filter(faculty = obj)
        return TestBaseSerializer(test,many = True).data
        

class AnswerBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerDB
        fields = ["id","answer","answer_picture","is_true"]
    
class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerBaseSerializer(many = True)

    class Meta:
        model = QuestionDB
        fields = ["id","question","question_img","answers"]


class SubjectSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model  = Subject
        fields = ["id","subject_name","questions"]

class TestDetailSerializer(serializers.ModelSerializer):
    faculty_id = serializers.IntegerField(write_only=True)
    subjects = SubjectSerializer(many=True)
    
    class Meta:
        model = TestDB
        fields = ["faculty_id","id",'test_name',"time","XP","subjects"]

    def create(self, validated_data):
        faculty_id = validated_data.pop("faculty_id")
        subjects_data = validated_data.pop("subjects")
        test = TestDB.objects.create(faculty_id = faculty_id,**validated_data)

        for subject_data in subjects_data:
            questions_data = subject_data.pop("questions")
            subject = Subject.objects.create(test=test, **subject_data)

            for question_data in questions_data:
                answers_data = question_data.pop("answers")
                question = QuestionDB.objects.create(subject=subject, **question_data)

                for answer_data in answers_data:
                    AnswerDB.objects.create(question=question, **answer_data)

        return test
    
    # def update(self, instance, validated_data):
    #     instance.test_name = validated_data.get("test_name", instance.test_name)
    #     instance.time = validated_data.get("time", instance.time)
    #     instance.XP = validated_data.get("XP", instance.XP)
    #     instance.faculty_id = validated_data.get("faculty_id", instance.faculty_id)
    #     instance.save()

    #     subjects_data = validated_data.pop("subjects", [])

    #     existing_subjects = {s.id: s for s in instance.subjects.all()}
    #     new_subject_ids = []

    #     for subject_data in subjects_data:
    #         questions_data = subject_data.pop("questions")
    #         subject_id = subject_data.get("id")

    #         if subject_id and subject_id in existing_subjects:
    #             subject = existing_subjects[subject_id]
    #             subject.subject_name = subject_data.get("subject_name", subject.subject_name)
    #             subject.save()
    #         else:
    #             subject = Subject.objects.create(test=instance, **subject_data)

    #         new_subject_ids.append(subject.id)

    #         existing_questions = {q.id: q for q in subject.questions.all()}
    #         new_question_ids = []

    #         for question_data in questions_data:
    #             answers_data = question_data.pop("answers")
    #             question_id = question_data.get("id")

    #             if question_id and question_id in existing_questions:
    #                 question = existing_questions[question_id]
    #                 question.question = question_data.get("question", question.question)
    #                 question.question_img = question_data.get("question_img", question.question_img)
    #                 question.save()
    #             else:
    #                 question = QuestionDB.objects.create(subject=subject, **question_data)

    #             new_question_ids.append(question.id)

    #             existing_answers = {a.id: a for a in question.answers.all()}
    #             new_answer_ids = []

    #             for answer_data in answers_data:
    #                 answer_id = answer_data.get("id")

    #                 if answer_id and answer_id in existing_answers:
    #                     answer = existing_answers[answer_id]
    #                     answer.answer = answer_data.get("answer", answer.answer)
    #                     answer.answer_picture = answer_data.get("answer_picture", answer.answer_picture)
    #                     answer.is_true = answer_data.get("is_true", answer.is_true)
    #                     answer.save()
    #                 else:
    #                     answer = AnswerDB.objects.create(question=question, **answer_data)

    #                 new_answer_ids.append(answer.id)

    #             # Optional: delete removed answers
    #             for answer in question.answers.all():
    #                 if answer.id not in new_answer_ids:
    #                     answer.delete()

    #         # Optional: delete removed questions
    #         for question in subject.questions.all():
    #             if question.id not in new_question_ids:
    #                 question.delete()

    #     # Optional: delete removed subjects
    #     for subject in instance.subjects.all():
    #         if subject.id not in new_subject_ids:
    #             subject.delete()

    #     return instance



#question detail Serializer
class QuestionDetailSerializer(serializers.ModelSerializer):
    
    answers = AnswerBaseSerializer(many = True)
    class Meta:
        model = QuestionDB
        fields = ["id","question","question_img","answers"]