from flask import request
from data.base_data import BaseData
from data.runs_manager import RunsManager

app = BaseData.app

@app.route("/api/v1/get_run_data", methods=["GET"])
def get_run_data():
    data: dict = request.get_json(force = True)
    if not data:
        return {"success": False, "error": "json not provided"}, 400
    
    run_uuid: str = data.get("uuid", None)
    if not run_uuid:
        return {"success": False, "error": "uuid not provided"}, 400

    run = RunsManager.get_run(run_uuid)
    if not run:
        return {"success": False, "error": "run doesn't exist"}, 400

    return {
        "success": True,
        "current_question": run.current_question,
        "questions": run.questions,
        "free_browsing": run.free_browsing
    }, 200