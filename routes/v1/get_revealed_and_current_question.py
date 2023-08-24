from flask import request
from data.base_data import BaseData
from data.questions_data import QuestionsData
from data.runs_manager import RunsManager

app = BaseData.app

@app.route("/api/v1/get_revealed_and_current_question", methods=["GET"])
def get_question():
    data: dict = request.get_json(force = True)
    if not data:
        return {"success": False, "error": "json not provided"}, 400
    
    run_uuid: str = data.get("uuid", None)
    if not run_uuid:
        return {"success": False, "error": "uuid not provided"}, 400

    run = RunsManager.get_run(run_uuid)
    if not run:
        return {"success": False, "error": "run doesn't exist"}, 400

    question_number = data.get("question_number")
    if not question_number:
        return {"success": False, "error": "question_number not provided"}, 400
    question_number = int(question_number)

    if question_number > run.question_count:
        return {"success": False, "error": "question_number higher than the run question count"}, 400

    if not run.can_access(question_number - 1):
        return {"success": False, "error": "tried to access an inaccessible question number (probably too high)"}, 403

    run.current_question = question_number

    revealed_questions: list[dict] = []
    current_question: dict | None = None
    
    # Grab the revealed questions (& if current question in there grab it revaled too)
    for i in run.revealed_questions:
        c_theme, c_hash = run.questions[i]
        if (i - 1 == question_number): 
            current_question = QuestionsData.questions_dict[c_theme][c_hash].get_dict_full()
        else:
            revealed_questions.append(QuestionsData.questions_dict[c_theme][c_hash].get_dict_full())

    # If current question wasn't grabbed above as revealed, grab it norally
    if not current_question:
        theme, hash = run.questions[question_number - 1]
        current_question = QuestionsData.questions_dict[theme][hash].get_dict_no_full_answer()

    return {
        "success": True,
        "revealed_questions": revealed_questions,
        "current_question": current_question
    }, 200