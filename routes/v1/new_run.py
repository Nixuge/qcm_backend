from flask import request
from data.base_data import BaseData
from uuid import uuid4
from data.runs_manager import RunsManager

from data.types.run import Run, RunBuilder

app = BaseData.app

@app.route("/api/v1/new_run", methods=["POST"])
def new_run():
    data: dict = request.get_json(force = True)
    if not data:
        return {"success": False, "error": "json not provided"}, 403
    
    included_themes: list[str] = data["theme"]
    question_count: int = data.get("question_count", 10)
        
    run = RunBuilder(
        selected_themes = included_themes,
        question_count = question_count
    ).build()

    if (type(run) == str):
        return {"success": False, "error": run}, 500

    RunsManager.add_run(run)
    return {"success": True, "code": run.uuid, "questions": run.questions}, 200

    
