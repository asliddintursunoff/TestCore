# api/utils/dtm_random.py
import random
from typing import Optional
from api.models.dtm_TEST import DTM_Subjects, DTM_Test_Language, Test

def pick_random_test_id(subject: DTM_Subjects, lang: DTM_Test_Language) -> Optional[int]:
    ids = list(
        Test.objects.filter(subject_name=subject, language=lang)
        .values_list("id", flat=True)
    )
    if not ids:
        return None
    return random.choice(ids)
