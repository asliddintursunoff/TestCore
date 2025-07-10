from rest_framework import serializers
from api.models.DTMtestDB import (DTMTestDB,
                                  DTMSubject,
                                  DTMQuestionDB,
                                  DTMAnswerDB,
                                  DTMTestGroups)
from rest_framework.reverse import reverse


#DTM tests groups serializer
class DTMTestGroupsSerializer(serializers.ModelSerializer):
    tests_link = serializers.SerializerMethodField()
    def get_tests_link(self, obj):
        request = self.context.get('request', None)
        return {
            "method": "GET",
            "label": "Get all tests belong to this group",
            "endpoint": reverse("dtm_tests", kwargs={"group_id": obj.id}, request=request),
           
        }
    class Meta:
        model = DTMTestGroups
        fields = ['id', 'group_name', 'subject1', 'subject2', 'tests_link']


#DTM tests filtered by group id 
class DTMTestsSerializer(serializers.ModelSerializer):
    test_link = serializers.SerializerMethodField(read_only = True)

    def get_test_link(self,obj):
        request = self.context.get("request",None)
        return{
            "method":"GET",
            "endpoint": reverse("dtm_test",kwargs={"id":obj.id},request=request)
        }
    class Meta:
        model = DTMTestDB
        fields = "__all__"


#for getting one DTM test
class DTMAnswerBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DTMAnswerDB
        fields = ["id","answer","answer_picture","is_true"]

class DTMQuestionBaseSerializer(serializers.ModelSerializer):
    DTManswers = DTMAnswerBaseSerializer(many = True)

    class Meta:
        model = DTMQuestionDB
        fields = ["id","question","question_img","DTManswers"]

class DTMSubjectBaseSerializer(serializers.ModelSerializer):
    DTMquestions = DTMQuestionBaseSerializer(many = True)

    class Meta:
        model = DTMSubject
        fields = ["id","subject_name","subject_score","DTMquestions"]


class DTMTestDetailSerializer(serializers.ModelSerializer):
    dtm_test_group_id = serializers.IntegerField(write_only = True)
    DTMsubjects = DTMSubjectBaseSerializer(many = True)

    class Meta:
        model = DTMTestDB
        fields = ["dtm_test_group_id","id","dtm_test_name","test_description","XP","DTMsubjects"]

    def create(self, validated_data):
        dtm_test_group_id = validated_data.pop("dtm_test_group_id")
        DTM_subjects_data = validated_data.pop("DTMsubjects")
        test = DTMTestDB.objects.create(dtm_test_group_id =dtm_test_group_id,**validated_data)

        for DTM_subject_data in DTM_subjects_data:
            DTMquestions_data = DTM_subject_data.pop("DTMquestions")
            subject = DTMSubject.objects.create(dtm_test = test,**DTM_subject_data)

            for DTMquestion_data in DTMquestions_data:
                DTManswers_data = DTMquestion_data.pop("DTManswers")
                question = DTMQuestionDB.objects.create(subject = subject,**DTMquestion_data)
                
                for answer_data in DTManswers_data:
                    DTMAnswerDB.objects.create(question = question,**answer_data)
        return test


    
