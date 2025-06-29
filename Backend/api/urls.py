from django.urls import path
from api.views.university_views import UniversityListAPIView,FacultyListAPIView
from api.views import test_result_views,test_views

urlpatterns = [
    path('university/',UniversityListAPIView.as_view()),
    path('faculties/<int:id>/',FacultyListAPIView.as_view()),
    path('tests/<int:faculty_id>/',test_views.TestsAPIView.as_view()),
    path("test/<int:id>/",test_views.TestDetailAPIView.as_view()),
    path("test-create/",test_views.FullTestCreateAPIView.as_view()),
    path("test-update/<int:id>/", test_views.FullTestUpdateAPIView.as_view()),
    path("submission-test/",test_result_views.TestSubmissionAPIView.as_view()),
    path("submission-test-result/<int:submitted_test_id>/",test_result_views.TestSubmittedResultAPIView.as_view())
]