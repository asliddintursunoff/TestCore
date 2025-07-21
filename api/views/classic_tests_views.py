
from api.models.ClassicTestDB import ClassicTestDB,ClassicQuestionDB
from rest_framework import generics
from rest_framework import permissions
from api.serializers.classic_testSZ import ClassicSubjectSerializer2,ClassicTestDBSerializer2,ClassicQuestionDBSerializer, ClassicBaseTestSerializer,ClassicTestDBSerializer
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse



@extend_schema(
    tags=["Classic Tests"],)
class ClassicTestListAPIView(generics.ListAPIView):
    serializer_class = ClassicBaseTestSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return ClassicTestDB.objects.filter(created_by=self.request.user)


@extend_schema(
    tags=["Classic Tests"],)
class ClassicTestDetailAPIView(generics.RetrieveAPIView):
    # serializer_class = ClassicTestDBSerializer()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id' 

    def get_queryset(self):
        return ClassicTestDB.objects.filter(created_by=self.request.user)
    
    def get_serializer(self, *args, **kwargs):
        kwargs['fields'] = ["created_by",'test_name', 'time', 'subjects']
        return ClassicTestDBSerializer(*args, **kwargs)



@extend_schema(
    tags=["Classic Tests"],)
class ClassicTestDetailforUniqueIDAPIView(generics.RetrieveAPIView):
    # serializer_class = ClassicTestDBSerializer()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'unique_code' 

    def get_queryset(self):
        return ClassicTestDB.objects.filter(created_by=self.request.user)
    
    def get_serializer(self, *args, **kwargs):
        kwargs['fields'] = ['id',"created_by",'test_name', 'time', 'subjects']
        return ClassicTestDBSerializer(*args, **kwargs)






@extend_schema(
    tags=["Classic Tests"],
    summary="Update a Classic Test",
    description="""
        This endpoint allows an authenticated user to update a Classic Test
        including its test name, duration, and associated subjects.
        Only the subjects' names and point values can be updated — questions and answers are untouched.
    """

)
class ClassicTestDetailUpdateAPIView(generics.RetrieveUpdateAPIView):

    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return ClassicTestDB.objects.filter(created_by=self.request.user)
    
    def get_serializer(self, *args, **kwargs):
        kwargs['fields'] = ['id','test_name', 'time','test_language','total_number_of_questions','difficulty','subjects']
        return ClassicTestDBSerializer2(*args, **kwargs)


@extend_schema(
    tags=["Classic Tests"],
    summary="Delete a Classic Test",
    description="Deletes a Test by ID. Must be authenticated.",
    responses={
        204: OpenApiResponse(description="Deleted successfully"),
        403: OpenApiResponse(description="Unauthorized or forbidden"),
        404: OpenApiResponse(description="Not found"),
    }
)
class ClassicTestDeleteAPIView(generics.DestroyAPIView):
    queryset = ClassicTestDB.objects.all()
    serializer_class = ClassicTestDBSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id' 

   


#questions    

@extend_schema(
    tags=["Classic Tests"],
    summary="Retrieve or Update a Classic Question",
    description="""
    This endpoint allows authenticated users to retrieve or update a single question
    and its nested answers. When updating, existing answers are replaced.
    """,
    request=ClassicQuestionDBSerializer,
    responses={
        200: OpenApiResponse(
            response=ClassicQuestionDBSerializer,
            description="Question retrieved or updated successfully.",
            examples=[
                OpenApiExample(
                    name="Update Payload Example",
                    value={
                        "id": 5,
                        "question": "What is 2 + 2?",
                        "question_img": None,
                        "answers": [
                            {"answer": "3", "is_true": False},
                            {"answer": "4", "is_true": True},
                            {"answer": "5", "is_true": False}
                        ]
                    },
                    request_only=True
                )
            ]
        )
    }
)


class  ClassicQuestionUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return ClassicQuestionDB.objects.filter()
    
    def get_serializer(self, *args, **kwargs):
        kwargs['fields'] =  ['id', 'question', 'question_img', 'answers']
        return ClassicQuestionDBSerializer(*args, **kwargs)


@extend_schema(
    tags=["Classic Tests"],
    summary="Delete a Classic Question",
    description="Deletes a single Classic Question by ID. Must be authenticated.",
    responses={
        204: OpenApiResponse(description="Deleted successfully"),
        403: OpenApiResponse(description="Unauthorized or forbidden"),
        404: OpenApiResponse(description="Not found"),
    }
)
class ClassicQuestionDeleteAPIView(generics.DestroyAPIView):
    queryset = ClassicQuestionDB.objects.all()
    serializer_class = ClassicTestDBSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id' 

   