from api.models.international_university_testDB import TestDB,QuestionDB
from api.models.DTMtestDB import DTMTestDB,DTMQuestionDB
import ast
import json
from rest_framework.exceptions import ParseError
import re

def calculating_earned_XP(test_id,total_questions_number,correct_answers_number):
    test = TestDB.objects.get(id = test_id)
    total_XP = test.XP
    total_questions_number = total_questions_number
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






def calculating_percentage(total_questions,total_true) -> float:
    return total_true/total_questions*100





def merge_questions(raw_list):
    grouped = {}  # Key: (subject_type, subject_name) → merged subject dict

    for item in raw_list:
        # Clean potential markdown
        clean_text = re.sub(r"^```json\n?|```$", "", item.strip())

        try:
            data = json.loads(clean_text)

            subject_type = data.get("subject_type", "").strip()
            subject_name = data.get("subject_name", "").strip()
            questions = data.get("questions", [])

            # Skip if missing fields or no questions
            if not (subject_type and subject_name and questions):
                continue

            key = (subject_type, subject_name)

            if key not in grouped:
                grouped[key] = {
                    "subject_type": subject_type,
                    "subject_name": subject_name,
                    "questions": []
                }

            grouped[key]["questions"].extend(questions)

        except json.JSONDecodeError as e:
            print(f"Skipping item due to JSON error: {e}")
            continue

    return {
        "subjects": list(grouped.values())
    }

