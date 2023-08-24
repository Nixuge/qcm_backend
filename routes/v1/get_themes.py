from data.base_data import BaseData
from data.questions_data import QuestionsData

app = BaseData.app

@app.route("/api/v1/get_themes", methods=["GET"])
def get_themes():
    return QuestionsData.themes