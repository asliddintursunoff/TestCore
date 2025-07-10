from rest_framework import serializers
from api.models.ClassicTestDB import ClassicTestDB, ClassicSubject, ClassicQuestionDB, ClassicAnswerDB

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
        fields = ['id', 'created_by', 'test_name', 'time', 'price_for_test', 'is_olympiad_test', 'subjects']

    def create(self, validated_data):
        subjects_data = validated_data.pop('subjects')
        test = ClassicTestDB.objects.create(**validated_data)
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
        subjects_data = validated_data.pop('subjects', [])
        instance.test_name = validated_data.get('test_name', instance.test_name)
        instance.time = validated_data.get('time', instance.time)
        instance.price_for_test = validated_data.get('price_for_test', instance.price_for_test)
        instance.is_olympiad_test = validated_data.get('is_olympiad_test', instance.is_olympiad_test)
        instance.save()

        # Recreate all subjects, questions, and answers
        instance.subjects.all().delete()
        for subject_data in subjects_data:
            questions_data = subject_data.pop('questions')
            subject = ClassicSubject.objects.create(test=instance, **subject_data)
            for question_data in questions_data:
                answers_data = question_data.pop('answers')
                question = ClassicQuestionDB.objects.create(subject=subject, **question_data)
                for answer_data in answers_data:
                    ClassicAnswerDB.objects.create(question=question, **answer_data)
        return instance
