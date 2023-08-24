import hashlib
import json
from data.questions_data import QuestionsData
from data.types.question import Question

def load_themes():
    with open("questions/THEMES.json", "r") as themesfile:
        QuestionsData.themes = json.load(themesfile)
    
def load_questions():
    load_themes()

    questions: dict[str, dict[str, Question]] = {}
    hashes: dict[str, list[str]] = {}

    for theme in QuestionsData.themes.keys():
        questions[theme] = {}
        hashes[theme] = []
        with open("questions/" + theme + ".json", "r") as themefile:
            questions_array: list[dict] = json.load(themefile)
        
        for question in questions_array:
            # Unique identifier for every question
            hash = hashlib.md5(json.dumps(question,sort_keys=True).encode('utf8')).hexdigest()
            hashes[theme].append(hash)

            questions[theme][hash] = Question.from_dict(question)
            

    QuestionsData.hashes = hashes
    QuestionsData.questions_dict = questions