import hashlib
import json
from data.questions_data import QuestionsData

def load_themes():
    with open("questions/THEMES.json", "r") as themesfile:
        QuestionsData.themes = json.load(themesfile)
    
def load_questions():
    load_themes()

    questions: dict[str, dict[str, dict]] = {}

    for theme, file in QuestionsData.themes.items():
        questions[theme] = {}
        with open("questions/" + file, "r") as themefile:
            questions_array = json.load(themefile)
        
        for question in questions_array:
            hash = hashlib.sha256(json.dumps(question,sort_keys=True).encode('utf8')).hexdigest()
            questions[theme][hash] = question

    QuestionsData.questions_dict = questions