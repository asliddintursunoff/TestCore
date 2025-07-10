from rest_framework import generics
from api.models.DTMtestDB import DTMTestGroups,DTMTestDB
from api.serializers.DTM_testSZ import DTMTestGroupsSerializer,DTMTestsSerializer,DTMTestDetailSerializer
from drf_spectacular.utils import extend_schema,extend_schema_view
from drf_spectacular.utils import OpenApiParameter,OpenApiExample
@extend_schema_view(
    get=extend_schema(tags=['DTM Universitetlari'],
                        summary="DTM testlarining guruhlanishi"))
class DTMTestGroupListAPIView(generics.ListAPIView):
    serializer_class = DTMTestGroupsSerializer
    queryset = DTMTestGroups.objects.all()


@extend_schema_view(
    get=extend_schema(
        tags=["DTM Universitetlari"],
        summary="DTM testlarni DTM test group ID si bilan filterlab olish",
        description="Returns a list of DTM tests that belong to a specific test group ID.",
        parameters=[
            OpenApiParameter(
                name="group_id",
                description="ID of the test group",
                required=True,
                type=int,
                location=OpenApiParameter.PATH
            )
        ]
    )
)
class DTMTestsListAPIView(generics.ListAPIView):
    serializer_class = DTMTestsSerializer
    def get_queryset(self):
        group_id = self.kwargs.get("group_id")      
        return DTMTestDB.objects.filter(id = group_id)
    
#for getting tests based on its ID
@extend_schema_view(
    get=extend_schema(
        tags=["DTM Universitetlari"],
        summary="Get a DTM test based on its ID",
        description="Retrieve full details of a DTM test using its ID."
    )
)
class DTMTestDetailAPIView(generics.RetrieveAPIView):
    queryset = DTMTestDB.objects.all()
    serializer_class = DTMTestDetailSerializer
    lookup_field = "id"

#for creating tests based on its ID
@extend_schema_view(
    post=extend_schema(
        tags=["DTM Universitetlari"],
        summary="Create full DTM test with one JSON",
        request=DTMTestDetailSerializer,
        responses={201: DTMTestDetailSerializer},
        examples=[
            OpenApiExample(
                name="Create DTM Test Example",
                value={
                    "dtm_test_group_id": 2,
                    "dtm_test_name": "Science Exam 2025",
                    "test_description": "Physics and Chemistry combined test",
                    "XP": 100,
                    "DTMsubjects": [
                        {
                            "subject_name": "Physics",
                            "subject_score": 3.1,
                            "DTMquestions": [
                                {
                                    "question": "What is Newton's second law?",
                                    "question_img": None,
                                    "DTManswers": [
                                        {"answer": "F = ma", "answer_picture": None, "is_true": True},
                                        {"answer": "E = mc^2", "answer_picture": None, "is_true": False},
                                    ]
                                }
                            ]
                        }
                    ]
                },
                request_only=True
            )
        ]
    )
)
class DTMTestFullCreateAPIView(generics.CreateAPIView):
    queryset = DTMTestDB.objects.all()
    serializer_class = DTMTestDetailSerializer
