from rest_framework import serializers
from api.models.ClassicTestDB import ClassicTestDB, ClassicSubject, ClassicQuestionDB, ClassicAnswerDB
from rest_framework.reverse import reverse
from django.core.files import File
import os
from django.conf import settings
import shutil

class ClassicAnswerDBSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassicAnswerDB
        fields = ['id', 'answer', 'answer_picture', 'is_true']

class ClassicQuestionDBSerializer(serializers.ModelSerializer):
    answers = ClassicAnswerDBSerializer(many=True)

    class Meta:
        model = ClassicQuestionDB
        fields = ['id', 'question', 'question_img', 'answers']

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        question = ClassicQuestionDB.objects.create(**validated_data)
        for answer_data in answers_data:
            ClassicAnswerDB.objects.create(question=question, **answer_data)
        return question

    def update(self, instance, validated_data):
        answers_data = validated_data.pop('answers', [])
        instance.question = validated_data.get('question', instance.question)
        instance.question_img = validated_data.get('question_img', instance.question_img)
        instance.save()

        # Handle answers: delete and recreate (simplest way)
        instance.answers.all().delete()
        for answer_data in answers_data:
            ClassicAnswerDB.objects.create(question=instance, **answer_data)
        return instance

class ClassicSubjectSerializer(serializers.ModelSerializer):
    questions = ClassicQuestionDBSerializer(many=True)

    class Meta:
        model = ClassicSubject
        fields = ['id', 'subject_name', 'point_for_each_question', 'questions']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        subject = ClassicSubject.objects.create(**validated_data)
        for question_data in questions_data:
            answers_data = question_data.pop('answers')
            question = ClassicQuestionDB.objects.create(subject=subject, **question_data)
            for answer_data in answers_data:
                ClassicAnswerDB.objects.create(question=question, **answer_data)
        return subject

    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions', [])
        instance.subject_name = validated_data.get('subject_name', instance.subject_name)
        instance.point_for_each_question = validated_data.get('point_for_each_question', instance.point_for_each_question)
        instance.save()

        # Recreate all questions and answers
        instance.questions.all().delete()
        for question_data in questions_data:
            answers_data = question_data.pop('answers')
            question = ClassicQuestionDB.objects.create(subject=instance, **question_data)
            for answer_data in answers_data:
                ClassicAnswerDB.objects.create(question=question, **answer_data)
        return instance

class ClassicTestDBSerializer(serializers.ModelSerializer):
    subjects = ClassicSubjectSerializer(many=True)

    class Meta:
        model = ClassicTestDB
        fields = ['id', 'created_by', 'test_name', 'time', 'price_for_test',"picture", 'is_olympiad_test', 'subjects']

    







    def create(self, validated_data):
        subjects_data = validated_data.pop('subjects')
        picture_path = validated_data.pop('picture', None)

        # Create the test object without the picture
        test = ClassicTestDB.objects.create(**validated_data)

        if picture_path:
            # Convert relative string to full path (adjust if needed)
            full_picture_path = os.path.join(settings.BASE_DIR, picture_path)
            print("Looking for image at:", full_picture_path)

            # Check if file exists
            if os.path.isfile(full_picture_path):
                with open(full_picture_path, 'rb') as f:
                    django_file = File(f)
                    test.picture.save(os.path.basename(picture_path), django_file, save=True)
                    print("✅ Picture saved successfully.")
            else:
                print("❌ Picture file not found:", full_picture_path)

        # Handle nested subjects/questions/answers
        for subject_data in subjects_data:
            questions_data = subject_data.pop('questions')
            subject = ClassicSubject.objects.create(test=test, **subject_data)
            for question_data in questions_data:
                answers_data = question_data.pop('answers')
                question = ClassicQuestionDB.objects.create(subject=subject, **question_data)
                for answer_data in answers_data:
                    ClassicAnswerDB.objects.create(question=question, **answer_data)

        return test






    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions', [])

        # Don't update the picture – just skip it if it exists in validated_data
        validated_data.pop('picture', None)

        instance.subject_name = validated_data.get('subject_name', instance.subject_name)
        instance.point_for_each_question = validated_data.get('point_for_each_question', instance.point_for_each_question)
        instance.save()

        # Recreate all questions and answers
        instance.questions.all().delete()
        for question_data in questions_data:
            answers_data = question_data.pop('answers')
            question = ClassicQuestionDB.objects.create(subject=instance, **question_data)
            for answer_data in answers_data:
                ClassicAnswerDB.objects.create(question=question, **answer_data)

        return instance




class ClassicBaseTestSerializer(serializers.ModelSerializer):
    # test_detail_api_endpoint = serializers.SerializerMethodField(help_text="API link to get detail of this test")
    
    

    # def test_detail_api_endpoint(self, obj):
    #     request = self.context.get('request', None)
    #     return {
    #         "method": "GET",
    #         "endpoint": reverse("getting_result", kwargs={"question_id": obj["id"],"test_type_id":2}, request=request),
          
    #     }
    
    class Meta:
        model = ClassicTestDB
        fields = ["id","created_by","test_name","time","picture"]