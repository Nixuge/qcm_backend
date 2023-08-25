from flask import request
from data.base_data import BaseData
from data.runs_manager import RunsManager

from data.types.run import RunBuilder

app = BaseData.app

@app.route("/api/v1/new_run", methods=["POST"])
def new_run():
    data: dict = request.get_json(force = True)
    if not data:
        return {"success": False, "error": "json not provided"}, 400
    
    included_themes: list[str] = data.get("theme", None)
    if not included_themes:
        return {"success": False, "error": "themes not provided in the json"}, 400

    free_browsing: bool = data.get("free_browsing", False)
    question_count: int = data.get("question_count", 10)
        
    run = RunBuilder(
        selected_themes = included_themes,
        question_count = question_count,
        free_browsing = free_browsing
    ).build()

    if (type(run) == str):
        return {"success": False, "error": run}, 500
    
    RunsManager.add_run(run) # type: ignore
    return {"success": True, "code": run.uuid, "questions": run.questions}, 200 # type: ignore

    
