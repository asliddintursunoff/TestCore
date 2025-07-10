from api.models.international_university_testDB import TestDB,QuestionDB
from api.models.DTMtestDB import DTMTestDB,DTMQuestionDB
import ast
import json
from rest_framework.exceptions import ParseError
import re

def calculating_earned_XP(test_id,correct_answers_number):
    test = TestDB.objects.get(id = test_id)
    total_XP = test.XP
    total_questions_number = QuestionDB.objects.filter(
                                                        subject__test=test
                                                        ).count()
    earned_XP =(total_XP*correct_answers_number)/total_questions_number 
    return earned_XP


def DTMcalculating_earned_XP(test_id,correct_answers_number):
    test = DTMTestDB.objects.get(id = test_id)
    total_XP = test.XP
    total_questions_number = DTMQuestionDB.objects.filter(
                                                        subject__dtm_test=test
                                                        ).count()
    earned_XP =(total_XP*correct_answers_number)/total_questions_number 
    return earned_XP






def merge_questions(raw_list):
    merged = {}
    all_questions = []

    for item in raw_list:
        # Remove markdown formatting if present
        clean_text = re.sub(r"^```json\n?|```$", "", item.strip())

        try:
            data = json.loads(clean_text)

            # Make sure it's the expected format
            if isinstance(data, dict) and "subject_name" in data and "questions" in data:
                subject_name = data["subject_name"]
                if not merged:
                    merged["subject_name"] = subject_name
                    merged["questions"] = []
                merged["questions"].extend(data["questions"])
        except json.JSONDecodeError as e:
            print(f"Skipping item due to JSON error: {e}")
            continue

    return {
        "subjects": [merged]
    }
