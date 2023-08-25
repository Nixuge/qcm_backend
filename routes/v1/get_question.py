from flask import request
from data.base_data import BaseData
from data.questions_data import QuestionsData
from data.runs_manager import RunsManager

app = BaseData.app

@app.route("/api/v1/get_question", methods=["GET"])
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

    theme, hash = run.questions[question_number - 1]  #list indexes start at 0

    question = QuestionsData.questions_dict[theme][hash]
    if question_number in run.revealed_questions:
        question_data = question.get_dict_full()
    else:
        question_data = question.get_dict_no_full_answer()

    return {
        "success": True,
        "question_data": question_data
    }, 200