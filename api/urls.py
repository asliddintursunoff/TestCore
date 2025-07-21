from django.urls import path
from api.views.international_university_views import UniversityListAPIView,FacultyListAPIView
from api.views import (dtm_test_result_views,
                       international_university_test_result_views, 
                       international_university_test_views, 
                       dtm_test_views,
                       ai_views,
                       all_test_type_views,
                       ai_question_making_views,
                       json_to_pdf_views,
                       classic_tests_views,
                       classic_test_result_views,
                       teacher_panel_views,
                       user_rating_views)
from api.views.authentication_views import TelegramOTPStoreAPIView, OTPVerifyJWTAPIView,CustomTokenRefreshView



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
    # listing classic tests belong to one user
    path("getting-classic-tests-belong-to-one-user/",classic_tests_views.ClassicTestListAPIView.as_view()),
    #main leader bord
    path("classic-test/<int:id>/",classic_tests_views.ClassicTestDetailAPIView.as_view()),
    #
    # GETTING test by its unique code
    path("classic-test/unique-code/<int:unique_code>/",classic_tests_views.ClassicTestDetailforUniqueIDAPIView.as_view(),name= "getting_test"),
    #
    #  GETTING Share data of classic test
    path("classic-test/shares/<int:id>/",teacher_panel_views.SHareTestRetrieveAPIView.as_view(),name= "getting_test"),
    #
    #classic test update
    path("classic-test-update/<int:id>/",classic_tests_views.ClassicTestDetailUpdateAPIView.as_view()),
    #
    #classic test update
    path("teacher-panel-leaderboard/<int:classic_test_id>/",user_rating_views.LeaderBoardForClassTestView.as_view()),
    #
    #classic test question update
    path("classic-test-question/<int:id>/",classic_tests_views.ClassicQuestionUpdateAPIView.as_view()),
    #
    #classic test question update
    path("classic-test/delete/<int:id>/",classic_tests_views.ClassicTestDeleteAPIView.as_view()),
    #sic test question delete
    path("classic-test-question/delete/<int:id>/",classic_tests_views.ClassicQuestionDeleteAPIView.as_view()),
    #
    #getting classic test pdf
    path("getting-test-teacherpanel-info/<int:classic_test_id>/",teacher_panel_views.Classic_Test_Utils_Views.as_view()),
    #
    #main leader bord
    path("main-leaderbord/",user_rating_views.LeaderboardView.as_view()),
    #
    

    #main leader bord
   
    #getting classic test pdf
    path("getting-test-pdf/<int:classic_test_id>/",json_to_pdf_views.GetClassicTestPDFbyID.as_view()),
    #
    #getting submitted classic test 
    path("classic-test/submit",classic_test_result_views.ClassicTestSubmissionAPIView.as_view()),
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
