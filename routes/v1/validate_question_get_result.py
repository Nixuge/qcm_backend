from flask import request
from data.base_data import BaseData
from data.questions_data import QuestionsData
from data.runs_manager import RunsManager

app = BaseData.app

@app.route("/api/v1/validate_question_get_result", methods=["GET"])
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

    # Todo: not sure about that one, but everytime you get a question it should set that 
    # so yeah
    # edit: scraped
    # if question_number != run.current_question:
    if not run.can_access(question_number - 1):
        return {"success": False, "error": "tried to access an inaccessible question number (probably too high)"}, 403

    answers = data.get("answers")
    if not answers:
        return {"success": False, "error": "answers not provided"}, 400
    
    answers_new = {}
    for key in [0, 1, 2]:
        answer = answers.get(key)
        if not answer:
            return {"success": False, "error": f"answers.{key} not provided"}, 400
        answers_new[key] = answer

    run.current_question = question_number

    theme, hash = run.questions[question_number - 1]  #list indexes start at 0

    run.add_submitted_answers(question_number, answers_new)

    return {
        "success": True,
        "question_result": QuestionsData.questions_dict[theme][hash].get_answer_only_dict()
    }, 200