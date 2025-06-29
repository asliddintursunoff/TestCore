from django.contrib import admin

from api.models.universityDB import *
from api.models.testDB import *
from api.models.test_result import *
admin.site.register(UniversityDB)
admin.site.register(FacultyDB)
admin.site.register(TestDB)
admin.site.register(Subject)
admin.site.register(QuestionDB)
admin.site.register(AnswerDB)
admin.site.register(TestSubmission)
admin.site.register(AnswerSubmission)