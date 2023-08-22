import hashlib
import json
from data.questions_data import QuestionsData

def load_themes():
    with open("questions/THEMES.json", "r") as themesfile:
        QuestionsData.themes = json.load(themesfile)
    
def load_questions():
    load_themes()

    questions: dict[str, dict[str, dict]] = {}
    answers: dict[str, dict[str, dict]] = {}
    hashes: dict[str, list[str]] = {}

    for theme in QuestionsData.themes.keys():
        questions[theme] = {}
        answers[theme] = {}
        hashes[theme] = []
        with open("questions/" + theme + ".json", "r") as themefile:
            questions_array: list[dict] = json.load(themefile)
        
        for question in questions_array:
            # Unique identifier for every question
            hash = hashlib.md5(json.dumps(question,sort_keys=True).encode('utf8')).hexdigest()
            
            # Remove & store the answer values from the questions dict
            answers_dict = question.pop("answers")
            explanation = question.pop("explanation")
            explanation_audio = question.pop("explanation_audio")

            questions[theme][hash] = question
            answers[theme][hash] = {
                "answers": answers_dict,
                "explanation": explanation,
                "explanation_audio": explanation_audio
            }
            hashes[theme].append(hash)

    QuestionsData.hashes = hashes
    QuestionsData.answers_dict = answers
    QuestionsData.questions_dict = questions