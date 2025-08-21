from django.contrib import admin

from api.models.international_universityDB import *
from api.models.international_university_testDB import *
from api.models.international_university_test_result import *
from api.models.DTMtestDB import *
from api.models.test_typesDB import *
from api.models.dtm_test_result import *
from api.models.tariffDB import *
from api.models.ClassicTestDB import *
from api.models.userDB import User
import nested_admin
from api.models.ClasssicTestResultDB import *
from api.models.dtm_TEST import *





# registering tariffs
admin.site.register(Tariff)
#
admin.site.register(DTMTestGroups)
#DTM TEST registration


admin.site.register(DTM_Test_Language)
admin.site.register(DTM_Subjects)

class DTMAnswerInline(nested_admin.NestedTabularInline):
    model = Answer
    extra = 1

class DTMQuestionInline(nested_admin.NestedTabularInline):
    model = Question
    inlines = [DTMAnswerInline]
    extra = 1


class DTMTestAdmin(nested_admin.NestedModelAdmin):
    inlines = [DTMQuestionInline]
 
admin.site.register(Test,DTMTestAdmin)
#
#Classic TEST registration
class ClassicAnswerInline(nested_admin.NestedTabularInline):
    model = ClassicAnswerDB
    extra = 1

class ClassicQuestionInline(nested_admin.NestedTabularInline):
    model = ClassicQuestionDB
    inlines = [ClassicAnswerInline]
    extra = 1

class ClassicSubjectInline(nested_admin.NestedTabularInline):
    model = ClassicSubject
    inlines = [ClassicQuestionInline]
    extra = 1

class ClassicTestAdmin(nested_admin.NestedModelAdmin):
    inlines = [ClassicSubjectInline]
 
admin.site.register(ClassicTestDB,ClassicTestAdmin)
#

#International Universities
class FacultyInline(nested_admin.NestedTabularInline):
    model = FacultyDB
    extra = 1

class UniversityAdmin(nested_admin.NestedModelAdmin):
    inlines = [FacultyInline]
 
admin.site.register(UniversityDB,UniversityAdmin)
#International University Tests
class AnswerInline(nested_admin.NestedTabularInline):
    model = AnswerDB
    extra = 1

class QuestionInline(nested_admin.NestedTabularInline):
    model = QuestionDB
    inlines = [AnswerInline]
    extra = 1

class SubjectInline(nested_admin.NestedTabularInline):
    model = Subject
    inlines = [QuestionInline]
    extra = 1

class TestAdmin(nested_admin.NestedModelAdmin):
    inlines = [SubjectInline]
 
admin.site.register(TestDB,TestAdmin)
#


# #DTM submitted answers Admin View
# class DTMAnswerSubmittedInline(nested_admin.NestedTabularInline):
#     model = DTMAnswerSubmission
#     extra = 1

# class DTMSubjectSubmissionInline(nested_admin.NestedTabularInline):
#     inlines = [DTMAnswerSubmittedInline]
#     model = DTMSubjectsSubmissionDB
#     extra =1
# class DTMTestSubmittedAdmin(nested_admin.NestedModelAdmin):
#     inlines = [DTMSubjectSubmissionInline]

# admin.site.register(DTMTestSubmission,DTMTestSubmittedAdmin)
# #

admin.site.register(AllTestTypes)
admin.site.register(TestSubmission)
admin.site.register(AnswerSubmission)


admin.site.register(User)
# admin.site.register(TestTypeDB)

admin.site.register(ClassicTestSubmission)
admin.site.register(EducationLanguage)