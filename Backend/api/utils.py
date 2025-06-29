from api.models.testDB import TestDB,QuestionDB

def calculating_earned_XP(test_id,correct_answers_number):
    test = TestDB.objects.get(id = test_id)
    total_XP = test.XP
    total_questions_number = QuestionDB.objects.filter(
                                                        subject__test=test
                                                        ).count()
    earned_XP =(total_XP*correct_answers_number)/total_questions_number 
    return earned_XP