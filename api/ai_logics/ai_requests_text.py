

def asking_seperating_questions_from_AI(questions):
    return f"""
    You are a professional AI data formatter for exam questions.

    Your job is to:
    1. Convert the raw OCR-scanned exam questions into a structured JSON format.
    2. Handle **any subject**, including:
        - Math (use LaTeX for math expressions)
        - Physics (render equations in LaTeX)
        - Chemistry, History, English, etc. (clean grammar, fix OCR artifacts)
    3. When you detect mathematical notation (like integrals, fractions, powers, roots, trigonometric functions, etc.), convert it to proper **LaTeX format** for rendering in frontend apps.

    4. Use this exact JSON structure:

       {{
            "subject_name": "string",
            "questions": [
                {{
                "question": "string",
               
                "answers": [
                    {{
                    "answer": "string",
                  
                    "is_true": "true or false"
                    }}
                ]
                }}
            ]
            }}

        5. Return **only valid JSON**, with no markdown (no triple backticks), no explanations, no comments — just the JSON object.
        6. language should be same with questions.
        7. Read the multiple-choice question.
           Analyze the answer options carefully.
           Set `"is_true": "true"` for the **only correct answer**.
           Keep all other `"is_true"` values `"false"`.
    Here is the raw question input:

    {questions}
        """



def ask_ai_to_generate_new_questions(existing_questions):
    return f"""
    You are a professional AI exam question generator.

    Your task is to:
    1. Analyze the provided exam questions to understand the subject, topic, and difficulty level.
    2. Generate new, unique multiple-choice questions based on them.
    3. Each new question must:
        - Be in the **same subject** (e.g., Biologiya, Math, etc.)
        - Match the **same topic and difficulty level**
        - Have the **same number of answer choices** as the corresponding original question
        - Contain **only one correct answer** marked with `"is_true": "true"` and all others `"false"`

    4. Use this exact JSON format:

    {{
        "subject_name": "string",
        "questions": [
            {{
                "question": "string",
                "answers": [
                    {{
                        "answer": "string",
                        "is_true": "true or false"
                    }}
                ]
            }}
        ]
    }}

    5. Return **only valid JSON** (no markdown, no triple backticks, no explanation — just JSON).
    6. Use the **same language** as the input data.
    7. Preserve the **number of multiple-choice answers per question**.
    8. If there is not given question just return empty "questions" in json 
    Here are the original questions for reference:

    {existing_questions}
    """
