# api/views/dtm_random.py
from django.core import signing
from django.db.models import Prefetch
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse, OpenApiParameter

from api.models.dtm_TEST import (
    DTM_Subjects, DTM_Test_Language, Test, Question
)
from api.serializers.dtm_random import (
    SubjectOptionSerializer, LanguageOptionSerializer,
    DTMTestFilterByIdSerializer, QuestionSerializer
)
from api.utils.dtm_random import pick_random_test_id

SIGN_SALT = "dtm.random.bundle.v1"
TOKEN_MAX_AGE_SECONDS = 60 * 60 * 6  # 6 hours

def _sign(payload: dict) -> str:
    return signing.dumps(payload, salt=SIGN_SALT)

def _unsign(token: str) -> dict:
    return signing.loads(token, salt=SIGN_SALT, max_age=TOKEN_MAX_AGE_SECONDS)

# ----------------- GET: Subjects (options) -----------------
@extend_schema(
    operation_id="list_dtm_subject_options",
    description="List subjects for selection. Optional ?test_type=main_subject|mandatory_subject",
    parameters=[OpenApiParameter(name="test_type", required=False, type=str)],
    responses={200: OpenApiResponse(description="OK")},
)
class ListSubjectOptions(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ttype = request.query_params.get("test_type")
        if ttype in ("main_subject", "mandatory_subject"):
            qs = DTM_Subjects.objects.filter(test_type=ttype).order_by("subject_name")
            return Response(SubjectOptionSerializer(qs, many=True).data, status=200)

        main_qs = DTM_Subjects.objects.filter(test_type="main_subject").order_by("subject_name")
        mand_qs = DTM_Subjects.objects.filter(test_type="mandatory_subject").order_by("subject_name")
        return Response({
            "main_subjects": SubjectOptionSerializer(main_qs, many=True).data,
            "mandatory_subjects": SubjectOptionSerializer(mand_qs, many=True).data,
        }, status=200)

# ----------------- GET: Languages (options) -----------------
@extend_schema(
    operation_id="list_dtm_language_options",
    description="List languages for selection.",
    responses={200: OpenApiResponse(description="OK")},
)
class ListLanguageOptions(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = DTM_Test_Language.objects.all().order_by("language")
        return Response(LanguageOptionSerializer(qs, many=True).data, status=200)

# ----------------- POST: Random bundle by IDs (stateless) -----------------
@extend_schema(
    operation_id="create_dtm_random_bundle_by_ids",
    description="Generate random tests using subject IDs and language ID (stateless). "
                "Returns the picked tests **and** a signed token to retrieve the same set later.",
    request=DTMTestFilterByIdSerializer,
    responses={
        201: OpenApiResponse(description="Created (returns token and lightweight items)"),
        400: OpenApiResponse(description="Invalid data"),
        404: OpenApiResponse(description="Subject / language / tests not found"),
    },
    examples=[
        OpenApiExample(
            "Type 2 request (IDs)",
            value={"filter_type": 2, "language_id": 1, "first_subject_id": 10, "second_subject_id": 11},
            request_only=True,
        ),
    ],
)
class CreateDTMRandomBundleByIds(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        s = DTMTestFilterByIdSerializer(data=request.data)
        if not s.is_valid():
            return Response({"error": s.errors}, status=status.HTTP_400_BAD_REQUEST)
        data = s.validated_data

        lang = DTM_Test_Language.objects.filter(id=data["language_id"]).first()
        if not lang:
            return Response({"error": "language not found"}, status=404)

        ft = data["filter_type"]
        first = DTM_Subjects.objects.filter(id=data["first_subject_id"]).first()
        if not first or first.test_type != "main_subject":
            return Response({"error": "first_subject not found or not a main_subject"}, status=404)

        subjects = []
        if ft == 1:
            time = 180
            second = DTM_Subjects.objects.filter(id=data["second_subject_id"]).first()
            if not second or second.test_type != "main_subject":
                return Response({"error": "second_subject not found or not a main_subject"}, status=404)
            subjects = [first, second]

        elif ft == 2:
            time = 270
            second = DTM_Subjects.objects.filter(id=data["second_subject_id"]).first()
            if not second or second.test_type != "main_subject":
                return Response({"error": "second_subject not found or not a main_subject"}, status=404)
            m1 = DTM_Subjects.objects.filter(subject_name="Matematika", test_type="mandatory_subject").first()
            m2 = DTM_Subjects.objects.filter(subject_name="Ona tili",   test_type="mandatory_subject").first()
            m3 = DTM_Subjects.objects.filter(subject_name="Ingliz tili", test_type="mandatory_subject").first()
            if not all([m1, m2, m3]):
                return Response({"error": "mandatory subjects missing (Matematika, Ona tili, Ingliz tili)"}, status=404)
            subjects = [first, second, m1, m2, m3]

        elif ft == 3:
            time = 90
            subjects = [first]

        else:
            return Response({"error": "filter_type must be 1, 2 or 3"}, status=400)

        # Pick one random Test per subject
        test_ids = []
        for subj in subjects:
            tid = pick_random_test_id(subj, lang)
            if tid is None:
                return Response({"error": f"No tests for subject_id={subj.id} language_id={lang.id}"}, status=404)
            test_ids.append(tid)

        token = _sign({
            "uid": request.user.id,
            "language_id": lang.id,
            "filter_type": ft,
            "test_ids": test_ids,
            "time":time
        })

        # Return minimal info + token (frontend can immediately show subjects names and scores if needed)
        tests = list(Test.objects.filter(id__in=test_ids).select_related("subject_name", "language"))
        tests.sort(key=lambda t: test_ids.index(t.id))
        items = [
            {
                "position": i + 1,
                "test_id": t.id,
                "subject_id": t.subject_name.id,
                "subject_name": t.subject_name.subject_name,
                "score": t.score,
                "language_id": t.language.id,
            }
            for i, t in enumerate(tests)
        ]
        return Response({"token": token, "items": items}, status=201)

# ----------------- GET: Retrieve SAME random set with full Q&A -----------------
@extend_schema(
    operation_id="retrieve_dtm_random_bundle_full",
    description=(
        "Retrieve the previously generated random set (via signed token) and return a payload shaped like your example: "
        "top-level test meta + subjects -> questions -> answers.\n\n"
        "You can override top-level presentation with query params: "
        "`?test_name=...&time=90&xp=30&test_description=...`."
    ),
    # parameters=[
    #     OpenApiParameter(name="test_name", required=False, type=str),
    #     OpenApiParameter(name="time", required=False, type=int),
    #     OpenApiParameter(name="xp", required=False, type=int),
    #     OpenApiParameter(name="test_description", required=False, type=str),
    # ],
    responses={200: OpenApiResponse(description="OK"), 400: OpenApiResponse(description="Bad token"),
               401: OpenApiResponse(description="Wrong user"), 410: OpenApiResponse(description="Expired token")},
)
class RetrieveDTMRandomBundleFull(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, token: str):
        from django.core.signing import BadSignature, SignatureExpired
        try:
            payload = _unsign(token)
        except BadSignature:
            return Response({"error": "invalid token"}, status=400)
        except SignatureExpired:
            return Response({"error": "token expired"}, status=410)

        if payload.get("uid") != request.user.id:
            return Response({"error": "unauthorized token user"}, status=401)

        test_ids = payload.get("test_ids", [])
        # Prefetch Q&A to avoid N+1
        tests = list(
            Test.objects.filter(id__in=test_ids)
            .select_related("subject_name", "language")
            .prefetch_related(
                Prefetch("DTMquestions", queryset=Question.objects.prefetch_related("DTManswers"))
            )
        )
        tests.sort(key=lambda t: test_ids.index(t.id))

        # Build subjects: include subject name, each test's score, and all questions+answers
        subjects = []
        total_questions = 0
        for t in tests:
            q_ser = QuestionSerializer(t.DTMquestions.all(), many=True, context={"request": request})
            questions = q_ser.data
            total_questions += len(questions)
            subjects.append({
                "id": t.id,
                "subject_name": t.subject_name.subject_name,
                "score": t.score,
                "questions": questions,
            })

        # Top-level meta (you can override via query params)
        resp = {
            "test_language": payload.get("language_id"),
            "time":payload.get("time"),
            # "time": int(request.query_params.get("time", 90)),
            # "test_description": request.query_params.get("test_description", ""),
            # "XP": int(request.query_params.get("xp", 0)),
            "questions_number": total_questions,
            "subjects": subjects
            
        }
        # test_name = request.query_params.get("test_name")
        # if test_name is not None:
        #     resp["test_name"] = test_name

        return Response(resp, status=200)
