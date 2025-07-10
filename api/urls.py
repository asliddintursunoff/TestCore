from django.urls import path
from api.views.international_university_views import UniversityListAPIView,FacultyListAPIView
from api.views import (dtm_test_result_views,
                       international_university_test_result_views, 
                       international_university_test_views, 
                       dtm_test_views,
                       ai_views,
                       all_test_type_views,
                       ai_question_making_views,
                       json_to_pdf_views)
from api.views.authentication_views import TelegramOTPStoreAPIView, OTPVerifyJWTAPIView,CustomTokenRefreshView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    #registration
    path('telegram-login/', TelegramOTPStoreAPIView.as_view()),
    path('verify-otp/', OTPVerifyJWTAPIView.as_view()),
    path('token/refresh/', CustomTokenRefreshView.as_view()),
    #
    #ai question making urls
    path("taking-questions-from-file/",ai_question_making_views.TakingQuestionFromFileAPIView.as_view()),
    path("creating-new-questions-from-file/",ai_question_making_views.CreatingNewQuestionFromFileAPIView.as_view()),
    #
    #all test type
    path("getting-test-pdf/<int:classic_test_id>/",json_to_pdf_views.GetClassicTestPDFbyID.as_view()),
    #
    #all test type
    path("tests-groups/",all_test_type_views.AllTestTypeListAPIView.as_view()),

    path('international-universities/',UniversityListAPIView.as_view()),
    path('international-universities/<int:id>/faculties/',FacultyListAPIView.as_view()),
    path('tests/<int:faculty_id>/',international_university_test_views.TestsAPIView.as_view()),
    path("test/<int:id>/",international_university_test_views.TestDetailAPIView.as_view()),
    path("test-create/",international_university_test_views.FullTestCreateAPIView.as_view()),
    path("test-update/<int:id>/", international_university_test_views.FullTestUpdateAPIView.as_view()),
    path("international-university-test/submit/",international_university_test_result_views.TestSubmissionAPIView.as_view()),
    path("submission-test-result/<int:submitted_test_id>/",international_university_test_result_views.TestSubmittedResultAPIView.as_view()),
    path("ai/<int:test_type_id>/<int:question_id>/",ai_views.AskResultAPIView.as_view(),name="getting_result"),

    #DTM
    path("dtm-test-groups/",dtm_test_views.DTMTestGroupListAPIView.as_view()),
    path("dtm-tests/<int:group_id>/",dtm_test_views.DTMTestsListAPIView.as_view(),name= "dtm_tests"),
    path("dtm-test/<int:id>/",dtm_test_views.DTMTestDetailAPIView.as_view(),name= "dtm_test"),
    path("dtm-test/create/",dtm_test_views.DTMTestFullCreateAPIView.as_view(),name= "create_dtm_test"),
    path("dtm-test/submit/",dtm_test_result_views.DTMTestSubmissionAPIView.as_view(),name= "submit_dtm_test"),
    path("dtm-test/show-result/<int:submitted_dtm_test_id>/",dtm_test_result_views.DTMTestSubmittedResultAPIView.as_view(),name= "submit_dtm_test"),
]
